import logging

from fastapi import Depends

from app.api.repository import project_repository
from app.helpers.paging import PaginationParams
from app.schemas.sche_project import CreateProject


async def get_list_project(params: PaginationParams = Depends()):
    logging.info("===> get list project service <===")
    project = await project_repository.get_project(params)
    return {
        'data': project
    }


async def create_project(data: CreateProject):
    logging.info("===> create project service <===")
    project = await project_repository.create_project(data)
    return {
        'data': project
    }
