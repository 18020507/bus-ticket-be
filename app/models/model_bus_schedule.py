from sqlalchemy import Column, String, Integer, DateTime

from app.models.model_base import BareBaseModel


class BusSchedule(BareBaseModel):
    company_name = Column(String, index=True)
    travel_from = Column(String, index=True)
    travel_to = Column(String, index=True)
    start_location = Column(String, index=True)
    finish_location = Column(String, index=True)
    start_time = Column(String, index=True)
    end_time = Column(String, index=True)
    capacity = Column(Integer, index=True)
    ways = Column(Integer, index=True)
    start_time_back = Column(String, index=True, nullable=True)
    end_time_back = Column(String, index=True, nullable=True)
    space_left = Column(Integer, index=True)
    price = Column(String, index=True)
