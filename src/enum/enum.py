from enum import Enum


class ErrorResponseCodeEnum(Enum):
    EMPTY_OR_NULL_FIELD = 100
    INVALID_CREDENTIALS = 101
    DUPLICATE_DATA = 102
