import logging
from datetime import datetime
from botocore.exceptions import ClientError
from fastapi import HTTPException, Depends
from fastapi_sqlalchemy import db
from starlette import status

from app.api.repository import bus_schedule_repository
from app.helpers.paging import paginate, PaginationParams
from app.models.model_ticket import Ticket
from app.schemas.sche_base import DataResponse
from app.schemas.sche_booking_ticket import UpdateTicket
from app.schemas.she_booking_ticket import CreateBookingTicket


async def get_list_ticket(params: PaginationParams = Depends()):
    try:
        logging.info("===> get list ticket repository <===")
        _query = db.session.query(Ticket)
        list_ticket = paginate(model=Ticket, query=_query, params=params)
        return DataResponse().success_response(list_ticket)
    except ClientError as e:
        logging.error("===> Error bus_schedule_repository.get_list_bus_schedule <===")
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


async def get_ticket_detail(current_user):
    try:
        logging.info("===> get ticket detail <===")
        ticket = db.session.query(Ticket).filter_by(user_id=current_user.id).all()
        if ticket is None:
            raise Exception('Ticket not exist')
        return ticket
    except ClientError as e:
        logging.error("===> Error get ticket detail repository <===")
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


async def create_booking_ticket(data: CreateBookingTicket):
    try:
        logging.info("===> create bus schedule repository <===")
        new_ticket = Ticket(
            user_id=data.customer_id,
            number_of_passenger=data.number_of_passenger,
            bus_id=data.bus_id,
        )
        print('da vao')
        await bus_schedule_repository.update_space_left(data.bus_id, data.number_of_passenger)
        db.session.add(new_ticket)
        db.session.commit()
        return DataResponse().success_response(data)
    except ClientError as e:
        logging.error("===> Error booking_ticket_repository.create_booking_ticket <===")
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)


async def update_ticket(ticket_id: int, data: UpdateTicket):
    try:
        logging.info("===> update ticket repository <===")
        current_time = datetime.now()
        current_ticket = db.session.query(Ticket).get(ticket_id)
        if current_ticket is None:
            raise Exception('Ticket not exist')
        current_ticket.updated_at = current_time
        if data.is_done is True:
            bus_detail = await bus_schedule_repository.get_bus_schedule_detail(current_ticket.bus_id)
            if bus_detail[0].space_left < current_ticket.number_of_passenger:
                raise Exception('No space left')
            else:
                current_ticket.is_done = True
                await bus_schedule_repository.update_space_left(current_ticket.bus_id,
                                                                current_ticket.number_of_passenger)
        db.session.commit()
        return DataResponse().success_response(data=current_ticket)
    except ClientError as e:
        logging.error("===> Error update_ticket <===")
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e.response)
