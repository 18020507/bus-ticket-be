import logging
from typing import Optional

from botocore.exceptions import ClientError
from fastapi import APIRouter, Depends, HTTPException, Form
from starlette import status

from app.api.service import bus_schedule_service, booking_ticket_service
from app.api.service.auth_service import UserService
from app.helpers.login_manager import login_required
from app.helpers.paging import PaginationParams
from app.models import User
from app.schemas.sche_booking_ticket import UpdateTicket
from app.schemas.she_booking_ticket import CreateBookingTicket

from config.route import Route

router = APIRouter()


@router.get(Route.V1.GET_TICKET_DETAIL, dependencies=[Depends(login_required)])
async def get_list_ticket(params: PaginationParams = Depends()):
    logging.info("===> function get_list_ticket <===")
    try:
        return await booking_ticket_service.get_list_ticket(params)
    except ClientError or Exception as e:
        logging.info("===>>> Error bus_schedule_controller.get_list_bus_schedule <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


@router.get(Route.V1.GET_LIST_BOOKING_TICKET, dependencies=[Depends(login_required)])
async def get_ticket_detail(current_user: User = Depends(UserService().get_current_user)):
    logging.info("===> function get_list_bus_schedule <===")
    try:
        return await booking_ticket_service.get_ticket_detail(current_user)
    except ClientError or Exception as e:
        logging.info("===>>> Error booking_ticket_controller.get_ticket_detail <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


@router.post(Route.V1.CREATE_BOOKING_TICKET, dependencies=[Depends(login_required)])
async def create_booking_ticket(user_id: int = Form(...), number_of_passenger: int = Form(...),
                                bus_id: int = Form(...)):
    logging.info("===> function create_booking_ticket <===")
    try:
        request_data = CreateBookingTicket(**{
            'customer_id': user_id,
            'number_of_passenger': number_of_passenger,
            'bus_id': bus_id,
        })
        return await booking_ticket_service.create_booking_ticket(request_data)
    except ClientError or Exception as e:
        logging.info("===>>> Error booking_ticket_controller.create_booking_ticket <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


@router.put(Route.V1.UPDATE_TICKET, dependencies=[Depends(login_required)])
async def update_ticket(ticket_id: int, is_done: Optional[bool]):
    logging.info("===> function update_ticket <===")
    try:
        request_data = UpdateTicket(**{
            "is_done": is_done
        })
        return await booking_ticket_service.update_ticket(ticket_id, request_data)
    except ClientError or Exception as e:
        logging.info("===>>> Error project_controller.create_project <<<===")
        logging.info(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)
