from sqlalchemy import Column, String, Boolean, DateTime

from app.models.model_base import BareBaseModel


class Project(BareBaseModel):
    project_name = Column(String, index=True)
    deleted_at = Column(DateTime)
