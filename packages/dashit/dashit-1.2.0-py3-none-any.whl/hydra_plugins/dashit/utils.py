import submitit

"""
    DashExecutor extends the functionality of submitit for Hydra-based applications. 
    It allows users to set a custom command that will be executed by the submitit plugin.
    '_submitit_command_str' provides a way to set the custom command, and
    falls back to the default pickle behavior if no custom command is set.
"""

class DashExecutor:    
    command = None

    @property
    def _submitit_command_str(self) -> str:
        # Returns the command if set, otherwise fallback to the super's command
        return self.command or super()._submitit_command_str

# Both classes need to override _submitit_command_str but they inherit from a different base class
class DashSlurmExecutor(DashExecutor, submitit.SlurmExecutor):
    pass

class DashLocalExecutor(DashExecutor, submitit.LocalExecutor):
    pass
