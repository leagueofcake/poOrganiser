class Error(Exception):
    """Base class for exceptions"""
    pass


class UserRegisteredError(Error):
    """Raised when attempting to register a User that already exists in the database."""
    pass


class UserNotFoundError(Error):
    """Raised when attempting to unregister or delete a User that does not exist in the database."""
    pass