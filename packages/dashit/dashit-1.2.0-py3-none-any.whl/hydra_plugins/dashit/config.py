# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Union, Optional
from hydra.core.config_store import ConfigStore
from pathlib import Path

@dataclass
class BaseQueueConf:
    """Configuration shared by all executors"""
    
    # name of the job
    name: str = "${hydra.job.name}"

    # default folder to store output, script, and pickle
    dashit_folder: str = "${hydra.sweep.dir}/dashit/%j"

    # number of nodes to use for the job
    nodes: int = 1
    
    # number of gpus to use on each node
    gpus_per_node: Optional[int] = None

    # number of cpus to use for each task
    cpus_per_task: Optional[int] = None

    # redirect stderr to stdout
    stderr_to_stdout: bool = True


# get all the config from submitit
@dataclass
class SlurmQueueConf(BaseQueueConf):
    """Slurm configuration overrides and specific parameters"""

    _target_: str = (
        "hydra_plugins.dashit.launcher.SlurmLauncher"
    )

    """
    Params are used to configure sbatch, for more info check:
    https://github.com/facebookincubator/submitit/blob/main/submitit/slurm/slurm.py

    Following parameters are slurm specific
    More information: https://slurm.schedmd.com/sbatch.html
    """
    
    partition: Optional[str] = None
    time: Optional[str] = None
    ntasks_per_node: Optional[int] = 1
    cpus_per_gpu: Optional[int] = None
    gpus_per_task: Optional[int] = None
    qos: Optional[str] = None  # quality of service
    mem: Optional[str] = None
    mem_per_gpu: Optional[str] = None
    mem_per_cpu: Optional[str] = None
    comment: Optional[str] = None
    constraint: Optional[str] = None
    exclude: Optional[str] = None
    account: Optional[str] = None
    gres: Optional[str] = None
    mail_type: Optional[str] = None
    mail_user: Optional[str] = None
    nodelist: Optional[str] = None
    dependency: Optional[str] = None
    exclusive: Optional[Union[bool, str]] = None
    wckey: str = "dashit"

    # Following parameters are submitit specifics

    # USR1 signal delay before timeout
    signal_delay_s: int = 120
    
    # Maximum number of retries on job timeout.
    # Change this only after you confirmed your code can handle re-submission
    # by properly resuming from the latest stored checkpoint.
    # check the following for more info on slurm_max_num_timeout
    # https://github.com/facebookincubator/submitit/blob/main/docs/checkpointing.md
    max_num_timeout: int = 0
    
    # Useful to add parameters which are not currently available in the plugin.
    # Eg: {"mail-user": "a.kamakshidasan@shell.com", "mail-type": "BEGIN"}
    additional_parameters: Dict[str, Any] = field(default_factory=dict)
    
    # Maximum number of jobs running in parallel
    array_parallelism: int = 256
    
    # A list of commands to run in sbatch before running srun
    setup: Optional[List[str]] = None
    
    # By default use srun
    use_srun: bool = True
    
    # Add each argument in the list to the srun call
    srun_args: Optional[List[str]] = None

@dataclass
class LocalQueueConf(BaseQueueConf):
    _target_: str = (
        "hydra_plugins.dashit.launcher.LocalLauncher"
    )

    # Only one node is supported for local executor
    
    timeout_min: Optional[float] = 120
    mem_gb: Optional[int] = None
    tasks_per_node: Optional[int] = 1

# finally, register two different choices:
ConfigStore.instance().store(
    group="hydra/launcher",
    name="dashit_local",
    node=LocalQueueConf(),
    provider="launcher",
)


ConfigStore.instance().store(
    group="hydra/launcher",
    name="dashit_slurm",
    node=SlurmQueueConf(),
    provider="launcher",
)
