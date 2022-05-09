from typing import Optional

from shared.domain import BaseError, Enum


class AnalyticsError(BaseError):
    def __init__(self, message: Optional[str] = None, *args, **kwargs) -> None:
        message = message or "Analytics Error"
        super().__init__(message, *args, **kwargs)


class AnalyticsGeneralMenu(Enum):
    ANALYTICS = "Analytics 📈"


class AnalyticsOptions(Enum):
    BY_MONTH = "Monthly"
    BY_YEAR = "Annually"


class AnalyticsDetailLevels(Enum):
    BASIC = "Basic"
    DETAILED = "Detailed"


class DetailReportExtraOptions(Enum):
    ALL = "🚛 All"
