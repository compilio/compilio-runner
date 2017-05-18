from enum import Enum


class TaskState(Enum):
    COMPILING = 1
    SUCCESS = 2
    ERROR = 3
