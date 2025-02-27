from models.users import UserModel
from werkzeug.security import safe_str_cmp


def authentication(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload["identity"]
    user = UserModel.find_by_id(user_id)
    return user
