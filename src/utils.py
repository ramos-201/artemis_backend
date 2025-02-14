from src.exceptions import EmptyOrNullFieldError


def is_field_null_or_empty(field) -> bool:
    return not (str(field or '').strip())


def validate_if_fields_are_not_empty_or_null(**fields) -> None:
    for key, value in fields.items():
        if is_field_null_or_empty(value):
            raise EmptyOrNullFieldError(f'The field "{key}" cannot be empty or contain only spaces.')
