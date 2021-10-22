from datetime import datetime, timedelta

from typing import List, Union, Tuple


def get_offset_week_days(return_offset: bool = False) -> Union[Tuple[List[str], int], List[str]]:
    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    min_date = datetime.now().date() - timedelta(days=6)
    min_day_index = min_date.weekday()
    offset_week_days = [week_days[week_day_index % 7] for week_day_index in range(min_day_index, min_day_index + 7)]
    if return_offset:
        return offset_week_days, min_day_index
    return offset_week_days


def offset_list(lst: List[int], offset_value: int) -> List[int]:
    lst_copy = lst.copy()
    return lst_copy[offset_value:] + lst[:offset_value]
