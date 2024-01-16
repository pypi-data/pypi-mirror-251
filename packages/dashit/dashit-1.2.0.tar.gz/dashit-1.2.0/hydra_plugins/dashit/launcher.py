# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from hydra.core.singleton import Singleton
from hydra.core.utils import JobReturn, filter_overrides, run_job, setup_globals
from hydra.errors import HydraException
from hydra.plugins.launcher import Launcher
from hydra.types import HydraContext, TaskFunction
from omegaconf import DictConfig, OmegaConf, open_dict

from .config import BaseQueueConf

from .utils import DashSlurmExecutor, DashLocalExecutor
from .constants import COMMANDS_TAG, BASH_TAG, INTERACTIVE_TAG, EXCEPTION_MESSAGE
from .status import tail_file, get_job_status
from hydra.core.utils import JobStatus

log = logging.getLogger(__name__)

class BaseSubmititLauncher(Launcher):

    _EXECUTOR = "abstract"

    def __init__(self, **params: Any) -> None:
        self.params = {}
        for k, v in params.items():
            if OmegaConf.is_config(v):
                v = OmegaConf.to_container(v, resolve=True)
            self.params[k] = v

        self.config: Optional[DictConfig] = None
        self.task_function: Optional[TaskFunction] = None
        self.sweep_configs: Optional[TaskFunction] = None
        self.hydra_context: Optional[HydraContext] = None

    def setup(
        self,
        *,
        hydra_context: HydraContext,
        task_function: TaskFunction,
        config: DictConfig,
    ) -> None:
        self.config = config
        self.hydra_context = hydra_context
        self.task_function = task_function

    def __call__(
        self,
        sweep_overrides: List[str],
        job_dir_key: str,
        job_num: int,
        job_id: str,
        singleton_state: Dict[type, Singleton],
    ) -> JobReturn:
        # lazy import to ensure plugin discovery remains fast
        import submitit

        assert self.hydra_context is not None
        assert self.config is not None
        assert self.task_function is not None

        Singleton.set_state(singleton_state)
        setup_globals()
        sweep_config = self.hydra_context.config_loader.load_sweep_config(
            self.config, sweep_overrides
        )

        with open_dict(sweep_config.hydra.job) as job:
            # Populate new job variables
            job.id = submitit.JobEnvironment().job_id  # type: ignore
            sweep_config.hydra.job.num = job_num

        return run_job(
            hydra_context=self.hydra_context,
            task_function=self.task_function,
            config=sweep_config,
            job_dir_key=job_dir_key,
            job_subdir_key="hydra.sweep.subdir",
        )

    def checkpoint(self, *args: Any, **kwargs: Any) -> Any:
        """Resubmit the current callable at its current state with the same initial arguments."""
        # lazy import to ensure plugin discovery remains fast
        import submitit

        return submitit.helpers.DelayedSubmission(self, *args, **kwargs)

    def launch(
        self, job_overrides: Sequence[Sequence[str]], initial_job_idx: int
    ) -> Sequence[JobReturn]:
        # lazy import to ensure plugin discovery remains fast
        import submitit

        assert self.config is not None

        num_jobs = len(job_overrides)
        assert num_jobs > 0
        params = self.params
        # build executor
        init_params = {"folder": self.params["dashit_folder"]}
        
        specific_init_keys = {"max_num_timeout"}

        init_params.update(
            **{
                f"{x}": y
                for x, y in params.items()
                if x in specific_init_keys
            }
        )
        
        init_keys = specific_init_keys | {"dashit_folder"}

        if self._EXECUTOR == SlurmLauncher._EXECUTOR:
            executor = DashSlurmExecutor(**init_params)
        else:
            executor = DashLocalExecutor(**init_params)

        # list of commands is expected to be a list
        commands = self.config.get(COMMANDS_TAG, None)

        # commands in the yaml file are expect to be a list,
        # remove new lines, join with semi-colons and add bash -c
        # give the command to the executor
        if commands:
            commands_list = [command.replace('\n', ' ') for command in commands]
            joined_command = "; ".join(commands_list)
            bash_command = f'{BASH_TAG} "{joined_command}"'
            executor.command = bash_command

        log.info(self._EXECUTOR + " + command: " + str(executor.command))

        # specify resources/parameters
        baseparams = set(OmegaConf.structured(BaseQueueConf).keys())
        
        params = {
            x if x in baseparams else f"{x}": y
            for x, y in params.items()
            if x not in init_keys
        }

        # "name" needs to be in the BaseQueueConf 
        # rename it to "job_name" for SlurmQueueConf
        params["job_name"] = params.pop("name")
        
        executor.update_parameters(**params)

        # Ensure sweep directory specified in Hydra config exists
        sweep_dir = Path(str(self.config.hydra.sweep.dir))
        sweep_dir.mkdir(parents=True, exist_ok=True)

        # set the directory permissions accordingly
        if "mode" in self.config.hydra.sweep:
            mode = int(str(self.config.hydra.sweep.mode), 8)
            os.chmod(sweep_dir, mode=mode)

        # Prepare job parameters list based on overrides
        job_params: List[Any] = []
        for idx, overrides in enumerate(job_overrides):
            idx = initial_job_idx + idx
            lst = " ".join(filter_overrides(overrides))
            log.info(f"\t#{idx} : {lst}")
            job_params.append(
                (
                    list(overrides),
                    "hydra.sweep.dir",
                    idx,
                    f"job_id_for_{idx}",
                    Singleton.get_state(),
                )
            )

        # Execute jobs using the specified executor and collect the results
        jobs = executor.map_array(self, *zip(*job_params))

        # If there's only one job and interactive = true in config
        # If there's multiple jobs, no printing on the terminal
        
        # tailing with local job is a catch-22
        # the current process is the process that needs to end
        # how will you find that process is over?!
        interactive = self.config.get(INTERACTIVE_TAG, False)
        if len(jobs) == 1 and interactive:
            job = jobs[0]
            tail_file(job.job_id, job.paths.stdout, self._EXECUTOR)
        
        processed_jobs = []

        # Get result from each job
        for job in jobs:
            job.wait()
            
            #if no command, then pkl file will be found, use results()
            if executor.command:
                job_status = get_job_status(job.state)

                if job_status != JobStatus.COMPLETED:
                    exception = HydraException(f"{EXCEPTION_MESSAGE}")
                    job_return = JobReturn(status=job_status, _return_value=exception)
                else:
                    job_return = JobReturn(status=job_status, _return_value=None)

                log.info(job.job_id + ": " + str(job_status))
            else:
                job_return = job.results()[0]
                log.info(job.job_id + ": " + str(job_return.status))
            
            processed_jobs.append(job_return)

        return processed_jobs

class LocalLauncher(BaseSubmititLauncher):
    _EXECUTOR = "local"


class SlurmLauncher(BaseSubmititLauncher):
    _EXECUTOR = "slurm"
