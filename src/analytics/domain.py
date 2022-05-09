from typing import Optional

from shared.domain import BaseError, CallbackItem, Enum, random_uuid
from storages import Storage


class AnalyticsError(BaseError):
    def __init__(self, message: Optional[str] = None, *args, **kwargs) -> None:
        message = message or "Analytics Error"
        super().__init__(message, *args, **kwargs)


class AnalyticsGeneralMenu(Enum):
    ANALYTICS = "Analytics 📈"


class ExtraCallbackData(Enum):
    MONTH_SELECTED = random_uuid()
    YEAR_SELECTED = random_uuid()
    CATEGORY_SELECTED = random_uuid()


class AnalyticsOptions(Enum):
    MONTHLY = CallbackItem(name="Monthly")
    ANNUALLY = CallbackItem(name="Annually")


class AnalyticsDetailLevels(Enum):
    BASIC = CallbackItem(name="Basic")
    DETAILED = CallbackItem(name="Detailed")


class DetailReportExtraOptions(Enum):
    ALL = CallbackItem(name="🚛 All")


class AnalyticsStorage(Storage):
    """slots: [account_id, option, category, date, detail_level]"""

    __slots__ = "account_id", "option", "category", "date", "detail_level"

    def __init__(self, account_id: int) -> None:
        if getattr(self, "__initialized", False):
            return

        super().__init__(account_id)
        self.option: Optional[AnalyticsOptions] = None
        self.date: Optional[str] = None
        self.detail_level: Optional[AnalyticsDetailLevels] = None
