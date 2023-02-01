from typing import Optional

from pydantic import BaseModel


class CreateBusSchedule(BaseModel):
    company_name: str
    travel_from: str
    travel_to: str
    start_location: str
    finnish_location: str
    start_time: str
    end_time: str
    capacity: int
    ways: int
    start_time_back: Optional[str] = ""
    end_time_back: Optional[str] = ""
    price: str


class UpdateBusSchedule(BaseModel):
    start_time: Optional[str] = ""
    end_time: Optional[str] = ""
    capacity: Optional[str] = ""
    ways: Optional[str] = ""
    price: Optional[str] = ""
