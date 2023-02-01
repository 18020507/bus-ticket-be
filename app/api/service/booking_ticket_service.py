import logging

from fastapi import Depends
from app.helpers.paging import PaginationParams
from app.api.repository import booking_ticket_repository, bus_schedule_repository
from app.schemas.sche_booking_ticket import UpdateTicket
from app.schemas.she_booking_ticket import CreateBookingTicket


async def get_list_ticket(params: PaginationParams = Depends()):
    logging.info("===> get list ticket service <===")
    list_ticket = await booking_ticket_repository.get_list_ticket(params)
    return {
        'data': list_ticket
    }


async def get_ticket_detail(current_user):
    logging.info("===> get ticket detail service <===")
    ticket = await booking_ticket_repository.get_ticket_detail(current_user)
    ticket_list = []
    for item in ticket:
        ticket_dict = item.__dict__
        bus_schedule = await bus_schedule_repository.get_bus_schedule_detail(item.bus_id)
        ticket_dict['bus_detail'] = bus_schedule[0]
        ticket_dict.pop('user_id')
        ticket_dict.pop('updated_at')
        ticket_dict.pop('bus_id')
        ticket_list.append(ticket_dict)
    user = {
        'full_name': current_user.full_name,
        'email': current_user.email
    }
    return {
        'data': ticket_list,
        'user': user
    }


async def create_booking_ticket(data: CreateBookingTicket):
    logging.info("===> create booking ticket service <===")
    booking_ticket = await booking_ticket_repository.create_booking_ticket(data)
    return booking_ticket


async def update_ticket(ticket_id: int, data: UpdateTicket):
    logging.info("===> update ticket service <===")
    ticket = await booking_ticket_repository.update_ticket(ticket_id, data)
    return {
        'data': ticket
    }
