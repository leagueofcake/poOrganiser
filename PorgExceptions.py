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


class DuplicateAttendanceError(Error):
    """Raised when attempting to create an Attendance object for a User that is already
    attending an Event."""
    pass


class AttendanceNotFoundError(Error):
    """Raised when an Attendance object is expected but cannot be found in the database."""
    pass


class ChoiceNotFoundError(Error):
    """Raised when a Choice object is expected but cannot be found in the database."""
    pass


class InvalidQuestionIdError(Error):
    """Raised when there are mis-matching question ids e.g. adding a choice to a response with
    different question ids"""
    pass


class QuestionNotFoundError(Error):
    """Raised when an Question object is expected but cannot be found in the database."""
    pass


class InvalidQuestionTypeError(Error):
    """Raised when a Question is given a question type that is not allowed by
    config.ALLOWED_QUESTION_TYPES"""
    pass


class ResponseNotFoundError(Error):
    """Raised when a Response object is expected but cannot be found in the database."""
    pass


class InvalidResponseError(Error):
    """Raised when a Response object is created that does not match the question_type of its
    parent Question."""
    pass


class SurveyNotFoundError(Error):
    """Raised when a Survey object is expected but cannot be found in the database."""
    pass
