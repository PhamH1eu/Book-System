class CustomException(Exception):
    """Base class for all custom exceptions."""

    def __init__(self, message: str, status_code: int = 500) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ResourceNotFoundException(CustomException):
    """Exception raised when a resource is not found."""

    def __init__(self, resource: str, resource_id: int) -> None:
        message = f"{resource} with ID {resource_id} not found."
        super().__init__(message, status_code=404)


class ResourceAlreadyExistsException(CustomException):
    """Exception raised when a resource already exists."""

    def __init__(self, resource: str, resource_id: int) -> None:
        message = f"{resource} with ID {resource_id} already exists."
        super().__init__(message, status_code=409)


class InvalidCredentialsException(CustomException):
    """Exception raised when credentials are invalid."""

    def __init__(self, message: str = "Invalid credentials.") -> None:
        super().__init__(message, status_code=401)


class InvalidTokenException(CustomException):
    """Exception raised when a token is invalid."""

    def __init__(self, message: str = "Invalid token.") -> None:
        super().__init__(message, status_code=401)


class UnauthorizedException(CustomException):
    """Exception raised when a user is not authorized."""

    def __init__(self, message: str = "Unauthorized access.") -> None:
        super().__init__(message, status_code=403)
