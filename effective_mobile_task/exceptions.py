class ApiException(Exception):
    def __init__(
        self, 
        status_code=500, 
        error="internal_error", 
        detail={},
        message=""
    ):
        self.status_code = status_code
        self.error = error
        self.detail = detail
        self.message = message

        super().__init__(f"{self.__class__.__name__}: {message}")


class NotFoundException(Exception):
    pass

class PermissionDeniedException(Exception):
    pass

class NotAuthorizedException(Exception):
    pass