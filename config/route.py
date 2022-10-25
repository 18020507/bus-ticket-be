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

        #         Project
        GET_LIST_PROJECT = '/project'
        CREATE_PROJECT = '/project'