import logging
from typing import Any

from botocore.exceptions import ClientError
from fastapi.security import OAuth2PasswordBearer

from app.api.service import auth_service
from app.api.service.auth_service import UserService
from app.models import User
from app.schemas.sche_base import DataResponse

from exception import handle_exception
from fastapi import APIRouter, Depends

from app.schemas.sche_user import Register, Login
from config.route import Route

router = APIRouter()


@router.post(Route.V1.LOGIN)
async def login(user: Login):
    logging.info("===>>> auth_controller.py <<<===")
    logging.info("===>>> function login <<<===")
    try:
        response = await auth_service.login(user=user)
        return response
    except ClientError or Exception as e:
        logging.error("===>>> Error auth_controller.login <<<===")
        logging.error(e)
        handle_exception.login_exception(e, user)


@router.post(Route.V1.REGISTER)
async def register(user_create: Register):
    logging.info("===>>> auth_controller.py <<<===")
    logging.info("===>>> function register <<<===")
    try:
        return await auth_service.register(user_create=user_create)
    except ClientError or Exception as e:
        logging.error("===>>> Error register <<<===")
        logging.error(e)
        handle_exception.sign_up_exception(e, user_create)


@router.get(Route.V1.GET_USER_DETAIL)
async def get_user_detail(current_user: User = Depends(UserService().get_current_user)) -> Any:
    return DataResponse().success_response(data=current_user)
    # logging.info("===>>> auth_controller.py <<<===")
    # logging.info("===>>> function get user detail <<<===")
    # try:
    #     oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    #     return UserService().get_current_user()
    #     # return await auth_service.get_user_detail(user_id)
    # except ClientError or Exception as e:
    #     logging.error("===>>> Error register <<<===")
    #     logging.error(e)


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = token
#     return user
#
#
# @router.get("/users/me")
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user
