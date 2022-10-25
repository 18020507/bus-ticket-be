class ErrorCode:
    MSG_LOGIN_INCORRECT = {
        # Incorrect username or password
        'code': 1,
        'message': 'LOGIN FAIL'
    }
    MSG_LOGIN_USERNAME_EMPTY = {
        # Username cannot be empty
        'code': 2,
        'message': 'USERNAME_EMPTY'
    }
    MSG_LOGIN_PASSWORD_EMPTY = {
        # Password cannot be empty
        'code': 3,
        'message': 'PASSWORD_EMPTY'
    }
    MSG_SIGNUP_EMAIL = {
        # Username should be an email
        'code': 4,
        'message': '!!!'
    }
    MSG_SIGNUP_EMAIL_EXISTS = {
        # An account with the given email already exists
        'code': 5,
        'message': '!!!'
    }
    MSG_SIGNUP_USER_LENGTH = {
        # Invalid length for username. Valid min length: 1
        'code': 6,
        'message': '!!!'
    }
    MSG_SIGNUP_PASSWORD_LENGTH = {
        # Invalid length for password. Valid min length: 6
        'code': 4,
        'message': '!!!'
    }


class OthersException:
    MESSAGES_ERROR_SIGN_UP = 'SIGN_UP ERROR'