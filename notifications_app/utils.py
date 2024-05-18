# notifications_app/utils.py
from home.middleware import get_current_user

def get_current_username():
    user = get_current_user()
    if user:
        return user.username
    return None
