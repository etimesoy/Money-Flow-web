import calendar
from datetime import datetime
from typing import Tuple, List


def get_offset_year_month(month_interval_offset: int) -> Tuple[int, int]:
    current_year, current_month = datetime.now().year, datetime.now().month
    current_month -= 1
    offset_year, offset_month = divmod(current_year * 12 + current_month + month_interval_offset, 12)
    offset_month += 1
    return offset_year, offset_month


def get_month_days_count(month_interval_offset: int) -> int:
    offset_year, offset_month = get_offset_year_month(month_interval_offset)
    _, month_days_count = calendar.monthrange(year=offset_year, month=offset_month)
    return month_days_count


def get_month_days(month_interval_offset: int) -> List[str]:
    offset_year, offset_month = get_offset_year_month(month_interval_offset)
    t = calendar.TextCalendar()
    month_name = t.formatmonthname(offset_year, offset_month, 0, withyear=False)
    c = calendar.Calendar()
    lst = list(map(lambda x: str(x) + ' ' + month_name, c.itermonthdays(offset_year, offset_month)))
    return list(filter(lambda x: int(x[0]) > 0, lst))
