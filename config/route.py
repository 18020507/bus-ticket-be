class Route:
    class V1:
        API = 'api'
        VERSION = 'v1'
        prefix_api = '/' + API + '/' + VERSION

        # HEALTHCHECK
        HEALTH_CHECK = '/'

        #         Auth
        LOGIN = '/login'
        REGISTER = '/register'
        GET_USER_DETAIL = '/user_detail'

        #         Project
        GET_LIST_PROJECT = '/project'
        CREATE_PROJECT = '/project'
        UPDATE_PROJECT = '/project'
        GET_PROJECT_DETAIL = '/project/{project_id}'

        #         Bus Schedule
        GET_LIST_BUS_SCHEDULE = '/bus_schedule'
        GET_LIST_DISTINCT_VALUE_OF_TRAVEL_FROM_FIELD = '/list_travel_from_field'
        GET_LIST_DISTINCT_VALUE_OF_TRAVEL_TO_FIELD = '/list_travel_to_field'
        CREATE_BUS_SCHEDULE = '/bus_schedule'
        UPDATE_BUS_SCHEDULE = '/bus_schedule/{bus_schedule_id}'
        GET_BUS_SCHEDULE = '/bus_schedule/{bus_schedule_id}'

        #         Booking ticket
        GET_TICKET_DETAIL = '/ticket_detail'
        GET_LIST_BOOKING_TICKET = '/list_ticket'
        CREATE_BOOKING_TICKET = '/booking_ticket'
        UPDATE_TICKET = '/booking_ticket/{ticket_id}'
