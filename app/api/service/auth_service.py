import logging
from datetime import datetime
from botocore.exceptions import ClientError
from app.schemas.sche_base import DataResponse
from app.schemas.sche_user import Register, Login
from app.core.security import create_access_token
import jwt

from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi_sqlalchemy import db
from pydantic import ValidationError
from starlette import status

from app.models import User
from app.core.config import settings
from app.core.security import verify_password, get_password_hash
from app.schemas.sche_token import TokenPayload
from app.schemas.sche_user import UserCreateRequest, UserUpdateMeRequest, UserUpdateRequest, UserRegisterRequest


async def login(user: Login):
    logging.info("===>>> auth_service.py <<<===")
    logging.info("===>>> function login <<<===")
    user = UserService().authenticate(email=user.username_id, password=user.password)
    if not user:
        raise HTTPException(status_code=400, detail='Incorrect email or password')
    elif not user.is_active:
        raise HTTPException(status_code=401, detail='Inactive user')

    user.last_login = datetime.now()
    db.session.commit()

    return {
        'access_token': create_access_token(user_id=user.id)
    }


async def register(user_create: Register):
    logging.info("===>>> auth_service.py <<<===")
    logging.info("===>>> function register <<<===")
    try:
        exist_user = db.session.query(User).filter(User.email == user_create.email).first()
        if exist_user:
            raise Exception('Email already exists')
        UserService().register_user(user_create)
        return {
            'full_name': user_create.full_name,
            'email': user_create.email,
            'role': user_create.role
        }
    except ClientError or Exception as e:  # ParamValidationError as e:
        logging.error("===>>> Error auth_service.register <<<===")
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail=e.response)


async def get_user_detail(user_id: str):
    ticket = db.session.query(User).get(user_id)
    return {
        'data': ticket
    }


class UserService(object):
    __instance = None

    reusable_oauth2 = HTTPBearer(
        scheme_name='Authorization'
    )

    @staticmethod
    def authenticate(*, email: str, password: str) -> Optional[User]:
        """
        Check username and password is correct.
        Return object User if correct, else return None
        """
        user = db.session.query(User).filter_by(email=email).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def get_current_user(http_authorization_credentials=Depends(reusable_oauth2)) -> User:
        """
        Decode JWT token to get user_id => return User info from DB query
        """
        try:
            payload = jwt.decode(
                http_authorization_credentials.credentials, settings.SECRET_KEY,
                algorithms=[settings.SECURITY_ALGORITHM]
            )
            token_data = TokenPayload(**payload)
        except(jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Could not validate credentials",
            )
        user = db.session.query(User).get(token_data.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    def register_user(data: Register):
        register_user = User(
            full_name=data.full_name,
            email=data.email,
            hashed_password=get_password_hash(data.password),
            is_active=True,
        )
        db.session.add(register_user)
        db.session.commit()
        return register_user

    @staticmethod
    def create_user(data: UserCreateRequest):
        new_user = User(
            full_name=data.full_name,
            email=data.email,
            hashed_password=get_password_hash(data.password),
            is_active=data.is_active,
            role=data.role.value,
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def update_me(data: UserUpdateMeRequest, current_user: User):
        current_user.full_name = current_user.full_name if data.full_name is None else data.full_name
        current_user.email = current_user.email if data.email is None else data.email
        current_user.hashed_password = current_user.hashed_password if data.password is None else get_password_hash(
            data.password)
        db.session.commit()
        return current_user

    @staticmethod
    def update(user: User, data: UserUpdateRequest):
        user.full_name = user.full_name if data.full_name is None else data.full_name
        user.email = user.email if data.email is None else data.email
        user.hashed_password = user.hashed_password if data.password is None else get_password_hash(
            data.password)
        user.is_active = user.is_active if data.is_active is None else data.is_active
        user.role = user.role if data.role is None else data.role.value
        db.session.commit()
        return user
