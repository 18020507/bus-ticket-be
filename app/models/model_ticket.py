from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean

from app.models.model_base import BareBaseModel


class Ticket(BareBaseModel):
    user_id = Column(Integer, ForeignKey('user.id'), index=True)
    number_of_passenger = Column(Integer, index=True)
    bus_id = Column(Integer, ForeignKey('busschedule.id'), index=True)
    is_done = Column(Boolean, default=False)
