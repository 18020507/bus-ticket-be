import logging
from datetime import datetime
from botocore.exceptions import ClientError
from fastapi import HTTPException, Depends
from fastapi_sqlalchemy import db
from starlette import status

from app.helpers.paging import paginate, PaginationParams
from app.models import BusSchedule
from app.schemas.sche_base import DataResponse
from app.schemas.sche_bus_schedule import CreateBusSchedule, UpdateBusSchedule


async def get_list_bus_schedule(travel_from: str, travel_to: str, ways: int, params: PaginationParams = Depends()):
    try:
        logging.info("===> get list bus schedule repository <===")
        _query = db.session.query(BusSchedule).filter_by(travel_from=travel_from, travel_to=travel_to, ways=ways)
        list_bus_schedule = paginate(model=BusSchedule, query=_query, params=params)
        return list_bus_schedule
    except ClientError as e:
        logging.error("===> Error bus_schedule_repository.get_list_bus_schedule <===")
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


async def get_list_distinct_value_of_travel_from_field():
    try:
        logging.info("===> get_list_distinct_value_of_travel_from_field repository <===")
        list_distinct_value_of_travel_from_field = db.session.query(BusSchedule.travel_from).distinct().all()
        return DataResponse().success_response(list_distinct_value_of_travel_from_field)
    except ClientError as e:
        logging.error("===> Error bus_schedule_repository.get_list_bus_schedule <===")
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


async def get_list_distinct_value_of_travel_to_field():
    try:
        logging.info("===> get_list_distinct_value_of_travel_to_field repository <===")
        list_distinct_value_of_to_from_field = db.session.query(BusSchedule.travel_to).distinct().all()
        return DataResponse().success_response(list_distinct_value_of_to_from_field)
    except ClientError as e:
        logging.error("===> Error bus_schedule_repository.get_list_bus_schedule <===")
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


async def create_bus_schedule(data: CreateBusSchedule):
    try:
        logging.info("===> create bus schedule repository <===")
        new_bus_schedule = BusSchedule(
            company_name=data.company_name,
            travel_from=data.travel_from,
            travel_to=data.travel_to,
            start_location=data.start_location,
            finish_location=data.finnish_location,
            start_time=data.start_time,
            end_time=data.end_time,
            capacity=data.capacity,
            ways=data.ways,
            start_time_back=data.start_time_back,
            end_time_back=data.end_time_back,
            space_left=data.capacity,
            price=data.price
        )
        db.session.add(new_bus_schedule)
        db.session.commit()
        return data
    except ClientError as e:
        logging.error("===> Error bus_schedule_repository.create_bus_schedule <===")
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


async def get_bus_schedule_detail(bus_id: int):
    try:
        logging.info("===> get_bus_schedule_detail <===")
        bus_schedule_detail = db.session.query(BusSchedule).filter_by(id=bus_id).all()
        if bus_schedule_detail is None:
            raise Exception('Bus schedule not exist')
        return bus_schedule_detail
    except ClientError as e:
        logging.error("===> Error get bus schedule detail repository <===")
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


async def update_space_left(bus_id: int, number_of_passenger: int):
    try:
        logging.info("===> update bus schedule repository <===")
        current_time = datetime.now()
        current_bus_schedule = db.session.query(BusSchedule).get(bus_id)
        if current_bus_schedule is None:
            raise Exception('Bus schedule not exist')
        if current_bus_schedule.space_left > number_of_passenger:
            current_bus_schedule.space_left = current_bus_schedule.space_left - number_of_passenger
            current_bus_schedule.updated_at = current_time
        db.session.commit()
        return current_bus_schedule
    except ClientError as e:
        logging.error("===> Error update space left <===")
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


async def update_bus_schedule(bus_id: int, data: UpdateBusSchedule):
    try:
        current_time = datetime.now()
        current_bus_schedule = db.session.query(BusSchedule).get(bus_id)
        current_bus_schedule.start_time = current_bus_schedule.start_time if data.start_time is None else data.start_time
        current_bus_schedule.end_time = current_bus_schedule.end_time if data.end_time is None else data.end_time
        current_bus_schedule.capacity = current_bus_schedule.capacity if data.capacity is None else data.capacity
        current_bus_schedule.ways = current_bus_schedule.ways if data.ways is None else data.ways
        current_bus_schedule.price = current_bus_schedule.price if data.price is None else data.price
        current_bus_schedule.updated_at = current_time
        if current_bus_schedule is None:
            raise Exception('Bus schedule not exist')
        db.session.commit()
        return DataResponse().success_response(data=current_bus_schedule)
    except ClientError as e:
        logging.error("===> Error update_bus_schedule <===")
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)
