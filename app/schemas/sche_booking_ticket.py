from pydantic import BaseModel


class CreateBookingTicket(BaseModel):
    user_id: int
    number_of_passenger: int
    bus_id: str


class UpdateTicket(BaseModel):
    is_done: bool



