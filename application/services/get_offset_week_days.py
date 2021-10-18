from datetime import datetime, timedelta


def get_offset_week_days():
    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    min_date = datetime.now().date() - timedelta(days=6)
    min_day_index = min_date.weekday()
    return [week_days[week_day_index % 7] for week_day_index in range(min_day_index, min_day_index + 7)]
