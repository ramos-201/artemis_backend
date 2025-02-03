from src.exceptions.exceptions import EmptyFieldError


PATH_API = '/graphql'


def is_field_null_or_empty(field) -> bool:
    return not (str(field or '').strip())


def validate_if_fields_are_not_empty_or_null(**fields) -> None:
    for key, value in fields.items():
        if is_field_null_or_empty(value):
            raise EmptyFieldError(f'The field "{key}" cannot be empty or contain only spaces.')
