from enum import Enum


class AvailabilityStatus(Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    TIME_RESTRICTED = "time_restricted"


class DiscountType(Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"

