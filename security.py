from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, 'bob', '1234')
]

username_mapping = {user.username: user for user in users}
userid_mapping = {user.id: user for user in users}


def authenticate(username, password):
    # if there isn't a user matching return None
    user = username_mapping.get(username, None)
    # safe way of comparing strings
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):  # payload = jwt content token
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
