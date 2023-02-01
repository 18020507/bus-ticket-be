from pydantic import BaseModel


class CreateBookingTicket(BaseModel):
    customer_id: int
    number_of_passenger: int
    bus_id: int

