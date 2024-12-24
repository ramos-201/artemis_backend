from src.models.user import User


class UserController:

    def __init__(self):
        self.model = User

    def create_user(self, name, last_name, username, email, mobile_phone, password):
        user_created = self.model.create(
            name=name, last_name=last_name, username=username, email=email,
            mobile_phone=mobile_phone, password=password, is_active_account=False,
        )

        return user_created
