import argparse
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


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Calculate the number of working days left in a given month."
    )
    parser.add_argument(
        "date", type=str, help="Date in DD/MM/YYYY format. "
        "The output from the program will be the number of working days left in "
        "the given month after the given date."
    )
    parser.add_argument(
        "-c", "--country", type=str, default=COUNTRY, help="Name of country to "
        "base working day calculation on. Country names are specified using "
        "ISO 3166-1 alpha-2 codes, such as UK, US, CA, etc."
    )
    parser.add_argument(
        "-s", "--subdiv", type=str, default=SUBDIV, help="Name of country "
        "subdivision to base working day calculation on. Subdivisions are "
        "specified using ISO 3166-2 codes, such as England, NY, ON, etc. "
        "For countries that don't have subdivisions, use None."
    )

    return parser.parse_args()
