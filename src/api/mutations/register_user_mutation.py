import graphene

from src.api.schemas.user_scheme import UserScheme
from src.controllers.user_controller import UserController
from src.exceptions.exceptions import DuplicateFieldError
from src.exceptions.exceptions import EmptyFieldError
from src.utils.utils import validate_if_fields_are_not_empty_or_null


class RegisterUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        mobile_phone = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
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
        except EmptyFieldError as e:
            return cls(
                ok=False,
                message=str(e),
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
        except DuplicateFieldError as e:
            return cls(
                ok=False,
                message=str(e),
                user=None,
            )

        return cls(
            ok=True,
            message='User registered successfully.',
            user=UserScheme(id=user_created.id),
        )
