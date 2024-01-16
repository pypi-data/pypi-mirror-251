import subprocess
import os
import time
from .constants import *
from hydra.core.utils import JobStatus

# Given a slurm job_id and output path, interactively print to terminal
def tail_file(job_id: str, job_path: str, platform: str):

    # currently local tailing is not implemented
    if platform == LOCAL_TAG:
        return
    
    print(f"Using batch job ID: {job_id}")
    print(f"\nTailing output file {job_path}")
    
    # There's a race condition initially, where file is not created by the time tail starts
    # but we know the file has been created
    while True:
        if os.path.exists(job_path):
            break
        time.sleep(1)
    
    tail_process = subprocess.Popen(TAIL_COMMAND + [job_path])
        
    try:
        # Use sacct and check whether the job has been completed
        while True:
            job_state = subprocess.check_output(SACCT_COMMAND + [job_id])
            job_state = job_state.decode().splitlines()[0].strip()
            if job_state in [COMPLETED_TAG, FAILED_TAG]:
                print(f"Job {job_id} has completed")
                break
            else:
                time.sleep(1)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        tail_process.terminate()

# Maps a job state string to a JobStatus enum for JobReturn
def get_job_status(state: str) -> JobStatus:
    status_mapping = {
        COMPLETED_TAG: JobStatus.COMPLETED,
        UNKNOWN_TAG: JobStatus.UNKNOWN,
        FAILED_TAG: JobStatus.FAILED,
        FINISHED_TAG: JobStatus.COMPLETED
    }
    return status_mapping.get(state, JobStatus.UNKNOWN)
