import calendar
import datetime
import sys

import holidays


COUNTRY = "UK"
SUBDIV = "England"


def calculate_working_days(
    given_date: str, country: str = COUNTRY, subdiv: str = SUBDIV,
) -> int:
 
    year, month, first_day = _split_date(given_date)
    month_length = _get_month_length(year, month)
    bank_holidays = _get_holidays(year, country, subdiv)

    working_days = 0

    for day in range(first_day + 1, month_length + 1):
        
        weekday = calendar.weekday(year, month, day)
        date = datetime.date(year, month, day)

        if weekday < 5 and date not in bank_holidays:
            working_days += 1
    
    return working_days


def _split_date(date: str) -> tuple[str, str, str]:
    date = datetime.datetime.strptime(date, "%d/%m/%Y")
    
    return (date.year, date.month, date.day)


def _get_month_length(year, month):
    return calendar.monthrange(year, month)[1]


def _get_holidays(year, country, subdiv):

    return holidays.country_holidays(
        years=year, country=country, subdiv=subdiv
    )
