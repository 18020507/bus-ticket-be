from fastapi import APIRouter

from app.api.controller import healthcheck_controller, auth_controller, project_controller, bus_schedule_controller, \
    booking_ticket_controller
from config.route import Route

router = APIRouter()

router.include_router(healthcheck_controller.router, prefix=Route.V1.prefix_api, tags=["Health-check"],
                      responses={404: {"description": "Not found"}})
router.include_router(auth_controller.router, prefix=Route.V1.prefix_api, tags=["Auth"],
                      responses={404: {"description": "Not found"}})
# router.include_router(project_controller.router, prefix=Route.V1.prefix_api, tags=["Project"],
#                       responses={404: {"description": "Not found"}})
router.include_router(bus_schedule_controller.router, prefix=Route.V1.prefix_api, tags=["Bus Schedule"],
                      responses={404: {"description": "Not found"}})
router.include_router(booking_ticket_controller.router, prefix=Route.V1.prefix_api, tags=["Booking Ticket"],
                      responses={404: {"description": "Not found"}})
