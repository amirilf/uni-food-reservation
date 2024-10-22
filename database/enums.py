import enum


class UserStage(enum.Enum):
    NEW = 1
    TERMS = 2
    LOGIN = 3
    PAID = 4