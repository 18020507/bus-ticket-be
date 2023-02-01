import logging
from typing import Optional

from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, HTTPException, Form
from starlette import status

from app.api.service import bus_schedule_service
from app.helpers.login_manager import login_required
from app.helpers.paging import PaginationParams
from app.schemas.sche_bus_schedule import CreateBusSchedule, UpdateBusSchedule

from config.route import Route

router = APIRouter()


@router.get(Route.V1.GET_LIST_BUS_SCHEDULE, dependencies=[Depends(login_required)])
async def get_list_bus_schedule(travel_from: str, travel_to: str, ways: int, params: PaginationParams = Depends()):
    logging.info("===> function get_list_bus_schedule <===")
    try:
        return await bus_schedule_service.get_list_bus_schedule(travel_from, travel_to, ways, params)
    except ClientError or Exception as e:
        logging.info("===>>> Error bus_schedule_controller.get_list_bus_schedule <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


@router.get(Route.V1.GET_LIST_DISTINCT_VALUE_OF_TRAVEL_FROM_FIELD, dependencies=[Depends(login_required)])
async def get_list_distinct_value_of_travel_from_field():
    try:
        return await bus_schedule_service.get_list_distinct_value_of_travel_from_field()
    except ClientError or Exception as e:
        logging.info("===>>> Error bus_schedule_controller.get_list_distinct_value_of_travel_from_field <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


@router.get(Route.V1.GET_LIST_DISTINCT_VALUE_OF_TRAVEL_TO_FIELD, dependencies=[Depends(login_required)])
async def get_list_distinct_value_of_travel_to_field():
    try:
        return await bus_schedule_service.get_list_distinct_value_of_travel_to_field()
    except ClientError or Exception as e:
        logging.info("===>>> Error bus_schedule_controller.get_list_distinct_value_of_travel_from_field <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


@router.post(Route.V1.CREATE_BUS_SCHEDULE, dependencies=[Depends(login_required)])
async def create_bus_schedule(company_name: str = Form(...), travel_from: str = Form(...), travel_to: str = Form(...),
                              start_location: str = Form(...), finnish_location: str = Form(...),
                              start_time: str = Form(...), end_time: str = Form(...),
                              capacity: int = Form(...), ways: int = Form(...),
                              start_time_back: Optional[str] = Form(None),
                              end_time_back: Optional[str] = Form(None), price: str = Form(...)):
    logging.info("===> function create_project <===")
    try:
        request_data = CreateBusSchedule(**{
            'company_name': company_name,
            'travel_from': travel_from,
            'travel_to': travel_to,
            'start_location': start_location,
            'finnish_location': finnish_location,
            'start_time': start_time,
            'end_time': end_time,
            'capacity': capacity,
            'ways': ways,
            'start_time_back': start_time_back,
            'end_time_back': end_time_back,
            'price': price
        })
        return await bus_schedule_service.create_bus_schedule(request_data)
    except ClientError or Exception as e:
        logging.info("===>>> Error bus_schedule_controller.create_bus_schedule <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


@router.put(Route.V1.UPDATE_BUS_SCHEDULE, dependencies=[Depends(login_required)])
async def update_bus_schedule(bus_id: int, start_time: Optional[str] = None, end_time: Optional[str] = None,
                              capacity: Optional[str] = None, ways: Optional[str] = None, price: Optional[str] = None):
    logging.info("===> function bus_schedule <===")
    try:
        request_data = UpdateBusSchedule(**{
            "start_time": start_time,
            "end_time": end_time,
            "capacity": capacity,
            "ways": ways,
            "price": price
        })
        return await bus_schedule_service.update_bus_schedule(bus_id, request_data)
    except ClientError or Exception as e:
        logging.info("===>>> Error booking_ticket_controller.update_bus_schedule <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)
