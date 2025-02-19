import graphene

from src.api.schemas.user_scheme import UserScheme
from src.controllers.user_controller import UserController
from src.enum import ErrorResponseCodeEnum
from src.exceptions import DuplicateFieldError
from src.exceptions import EmptyOrNullFieldError
from src.utils import validate_if_fields_are_not_empty_or_null


class RegisterUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        mobile_phone = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    code_error = graphene.Int()
    message = graphene.String()
    user = graphene.Field(UserScheme)

    @classmethod
    async def mutate(
            cls,
            root,
            info,
            name: str,
            last_name: str,
            username: str,
            email: str,
            mobile_phone: str,
            password: str,
    ):
        try:
            validate_if_fields_are_not_empty_or_null(
                name=name,
                last_name=last_name,
                username=username,
                email=email,
                mobile_phone=mobile_phone,
                password=password,
            )
        except EmptyOrNullFieldError as error:
            return cls(
                ok=False,
                code_error=ErrorResponseCodeEnum.EMPTY_OR_NULL_FIELD.value,
                message=str(error),
                user=None,
            )

        user_controller = UserController()
        try:
            user_created = await user_controller.create_user(
                name=name,
                last_name=last_name,
                username=username,
                email=email,
                mobile_phone=mobile_phone,
                password=password,
            )
        except DuplicateFieldError as error:
            return cls(
                ok=False,
                code_error=ErrorResponseCodeEnum.DUPLICATE_DATA.value,
                message=str(error),
                user=None,
            )

        return cls(
            ok=True,
            code_error=None,
            message='User registered successfully.',
            user=UserScheme(id=user_created.id),
        )
