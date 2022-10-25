import logging
from datetime import datetime

from botocore.exceptions import ClientError
from fastapi import HTTPException, Depends
from fastapi_sqlalchemy import db
from starlette import status

from app.helpers.paging import paginate, PaginationParams
from app.models import Project
from app.schemas.sche_project import CreateProject


async def get_project(params: PaginationParams = Depends()):
    try:
        logging.info("===> get list project repository <===")
        _query = db.session.query(Project)
        users = paginate(model=Project, query=_query, params=params)
        return users
    except ClientError as e:
        logging.error("===> Error project_repository.get_list_project <===")
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


async def create_project(data: CreateProject):
    try:
        logging.info("===> get create project repository <===")
        current_time = datetime.now()
        new_project = Project(
            project_name=data.project_name,
            created_at=current_time
        )
        db.session.add(new_project)
        db.session.commit()
        return new_project
    except ClientError as e:
        logging.error("===> Error project_repository.create_project <===")
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)
