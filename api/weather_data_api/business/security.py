import uuid
from datetime import datetime

from flask_jwt import JWTError
from passlib.hash import sha512_crypt
from sqlalchemy import and_

from database import db
from database.models import User


class PasswordException(Exception):
    """
    Exception on password
    """

    def __init__(self, message):
        """
        Constructor.

        :param message: The error message.
        :type message: str
        """
        self.message = message


def authenticate(username: str, password: str):
    """
    Authenticate a user using their username and a supplied password.

    :param username: The user's username.
    :type username: str
    :param password: The user's candidate password provided at login.
    :type password: str
    :return: A User object on success, else None.
    """
    try:
        user = User.query.filter(and_(User.username == username, User.enabled == 1)).one()

        if user.enabled and sha512_crypt.verify(password, user.password):
            update_last_login_date(username=username)
            return user
        else:
            return None
    except Exception as e:
        raise JWTError(error='Invalid credential', description='Stop hacking', status_code=401)


def username_is_available(username: str) -> bool:
    """
    Checks if the username is available.
    :param username: The username requested.
    :type username: str
    :return: True if the username is available, else False.
    """
    user_count = User.query.filter(User.username == username).count()

    if user_count > 0:
        return False

    return True


def create_user(data):
    """
    Create a user in the database.
    
    :param data: JSON data for a new User object.
    """
    user = None
    username = data.get('username')
    password = data.get('password')
    enabled = data.get('enabled')

    if username_is_available(username):
        salt = uuid.uuid4()
        encrypted_password = sha512_crypt.hash(password)
        enabled = False

        user = User(username=username,
                    password=encrypted_password,
                    enabled=enabled)
        db.session.add(user)
        db.session.commit()

    return user


def delete_user(username: str):
    """
    Delete a user record in the database.

    :param username: The username.
    :type username: str
    :return: None
    """
    user = User.query.filter(User.username == username).one()
    db.session.delete(user)
    db.session.commit()


def disable_user(username: str) -> User:
    """
    Disable a user in the database.

    :param username: The user's username.
    :return: User
    """
    user = User.query.filter(User.username == username).one()
    user.enabled = False

    db.session.add(user)
    db.session.commit()

    return user


def enable_user(username: str) -> User:
    """
    Enable a user in the database.

    :param username: The user's username.
    :return: User
    """
    user = User.query.filter(User.username == username).one()
    user.enabled = True

    db.session.add(user)
    db.session.commit()

    return user


def update_last_login_date(username: str) -> User:
    """
    Update a user's last login date.

    :param username: The user's username.
    :type username: str
    :return: None
    """
    user = User.query.filter(User.username == username).one()
    user.last_login_date = datetime.utcnow()

    user = db.session.add(user)
    db.session.commit()

    return user


def update_password(username: str, password: str, new_password: str) -> User:
    """
    Update a user's password.

    :param username: The user's username.
    :type username: str
    :param password: The user's current password.
    :type password: str
    :param new_password: The user's new password.
    :type new_password: str
    :return: User
    """
    user = User.query.filter(User.username == username).one()

    if sha512_crypt.verify(password, user.password):
        user.password = sha512_crypt.hash(password)
        db.session.add(user)
        db.session.commit()

        return user
    else:
        raise PasswordException(message='Current password is not correct.')


def identity(payload):
    user_id = payload['identity']
    user = User.query.filter(User.id == user_id).one()
    return user
