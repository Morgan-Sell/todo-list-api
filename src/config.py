from enum import Enum

# Postgres Connection Parameters
DB_NAME = "todo_list"
DB_HOST = "localhost"
DB_PORT = "5432"


class TaskStatus(Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


TASK_STATUS_LIST = [
    "Not Started",
    "In Progress",
    "Completed"
]