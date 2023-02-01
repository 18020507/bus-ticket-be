import logging

from fastapi import Depends

from app.api.repository import bus_schedule_repository
from app.helpers.paging import PaginationParams
from app.schemas.sche_bus_schedule import CreateBusSchedule, UpdateBusSchedule


async def get_list_bus_schedule(travel_from: str, travel_to: str, ways: int, params: PaginationParams = Depends()):
    logging.info("===> get list bus schedule service <===")
    list_bus_schedule = await bus_schedule_repository.get_list_bus_schedule(travel_from, travel_to, ways, params)
    return list_bus_schedule


async def get_list_distinct_value_of_travel_from_field():
    logging.info("===> get_list_distinct_value_of_travel_from_field service <===")
    list_distinct_value_of_travel_from_field = await bus_schedule_repository.get_list_distinct_value_of_travel_from_field()
    return list_distinct_value_of_travel_from_field


async def get_list_distinct_value_of_travel_to_field():
    logging.info("===> get_list_distinct_value_of_travel_to_field service <===")
    list_distinct_value_of_travel_from_field = await bus_schedule_repository.get_list_distinct_value_of_travel_to_field()
    return list_distinct_value_of_travel_from_field


async def create_bus_schedule(data: CreateBusSchedule):
    logging.info("===> create project service <===")
    bus_schedule = await bus_schedule_repository.create_bus_schedule(data)
    return {
        'data': bus_schedule
    }


async def update_bus_schedule(bus_id: int, data: UpdateBusSchedule):
    logging.info("===> update bus schedule service <===")
    ticket = await bus_schedule_repository.update_bus_schedule(bus_id, data)
    return {
        'data': ticket
    }
