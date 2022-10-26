from pydantic import BaseModel
from sqlalchemy import DateTime


class CreateProject(BaseModel):
    project_name: str


class UpdateProject(BaseModel):
    project_name: str
