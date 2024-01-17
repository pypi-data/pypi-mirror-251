"""This module contains all the exceptions used in the project."""


class InvalidPowerFactorException(Exception):
    """Raised when the power factor is not between 0 and 1."""

    pass


class MultipleDevicesException(Exception):
    """Raised when there are multiple devices associated with the account."""

    pass


class UnsupportedMethodException(Exception):
    """Raised when an unsupported method is used."""

    pass


class InvalidPlanException(Exception):
    """Raised when the plan is not valid."""

    pass


class TariffException(Exception):
    """Raised when the tariff is not valid."""

    pass


class ReadingRequestFailedException(Exception):
    """Raised when the reading request fails."""

    pass


class ReadingResponseInvalidException(Exception):
    """Raised when the reading response is invalid."""

    pass
