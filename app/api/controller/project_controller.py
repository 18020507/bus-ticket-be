import logging
from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, HTTPException, Form
from starlette import status, schemas

from app.api.service import project_service
from app.helpers.login_manager import login_required
from app.helpers.paging import PaginationParams
from app.schemas.sche_project import CreateProject

from config.route import Route

router = APIRouter()


@router.get(Route.V1.GET_LIST_PROJECT, dependencies=[Depends(login_required)])
async def get_list_project(params: PaginationParams = Depends()):
    logging.info("===> function get_list_project <===")
    try:
        return await project_service.get_list_project(params)
    except ClientError or Exception as e:
        logging.info("===>>> Error project_controller.get_list_project <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


@router.post(Route.V1.CREATE_PROJECT, dependencies=[Depends(login_required)])
async def create_project(project_name: str = Form(...)):
    logging.info("===> function create_project <===")
    try:
        request_data = CreateProject(**{
            'project_name': project_name,
        })
        return await project_service.create_project(request_data)
    except ClientError or Exception as e:
        logging.info("===>>> Error project_controller.create_project <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)
