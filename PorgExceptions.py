class Error(Exception):
    """Base class for exceptions"""
    pass


class UserRegisteredError(Error):
    """Raised when attempting to register a User that already exists in the database."""
    pass


class UserNotFoundError(Error):
    """Raised when a User object is expected but cannot be found in the database."""
    pass


class EventNotFoundError(Error):
    """Raised when an Event object is expected but cannot be found in the database."""
    pass


class AttendanceNotFoundError(Error):
    """Raised when an Attendance object is expected but cannot be found in the database."""
    pass