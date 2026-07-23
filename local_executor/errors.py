class ExecutorError(Exception):
    """Base class for expected, safely reportable executor failures."""


class TaskValidationError(ExecutorError):
    pass


class PolicyError(ExecutorError):
    pass


class ExecutionError(ExecutorError):
    pass
