"""
Take a date, calculate the number of working days left in the month,
and print the result.
"""
import argparse
import calendar
import datetime
import os
import sys

import holidays
from pyfiglet import figlet_format  # type: ignore
from termcolor import colored


COUNTRY = "GB"
SUBDIV = "England"


def calculate_working_days(
    given_date: str, country: str = COUNTRY, subdiv: str = SUBDIV
) -> int:
    """
    Take a date and calculate the number of working days
    left in the month.

    Args:
        given_date (str): Date to base calculation on.
        Format must be DD/MM/YYYY.

        country (str): Optional country to base the calculation on
        instead of the default country.

        subdiv (str): Optional country subdivison to base the calculation on
        instead of the default country subdivison.

    Returns:
        An integer representing the number of working days left in the month
        after the given date.

    """

    year, month, given_day = _split_date(given_date)
    month_length = _get_month_length(year, month)
    bank_holidays = _get_holidays(year, country, subdiv)

    working_days = 0

    for day in range(given_day + 1, month_length + 1):

        weekday = calendar.weekday(year, month, day)
        date = datetime.date(year, month, day)

        if weekday < 5 and date not in bank_holidays:
            working_days += 1

    return working_days


def _split_date(given_date: str) -> tuple[int, int, int]:
    date = datetime.datetime.strptime(given_date, "%d/%m/%Y")

    return (date.year, date.month, date.day)


def _get_month_length(year: int, month: int) -> int:
    return calendar.monthrange(year, month)[1]


def _get_holidays(year: int, country: str, subdiv: str) -> holidays.HolidayBase:
    if subdiv == "None":
        return holidays.country_holidays(years=year, country=country)

    return holidays.country_holidays(years=year, country=country, subdiv=subdiv)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate the number of working days left in a month.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "date",
        type=str,
        help="Date in DD/MM/YYYY format. "
        "The output from the program will be the number of working days left in "
        "the month after the given date.",
    )
    parser.add_argument(
        "-c",
        "--country",
        type=str,
        default=COUNTRY,
        help="Name of country to base working day calculation on. Country names are "
        "specified using ISO 3166-1 alpha-2 codes, such as GB, US, CA, etc. "
        "Most countries can also be specified by name (Canada, Turkey, etc.).",
    )
    parser.add_argument(
        "-s",
        "--subdiv",
        type=str,
        default=SUBDIV,
        help="Name of country subdivision to base working day calculation on. "
        "Subdivisions are specified using ISO 3166-2 codes, such as "
        "England, NY, ON, etc. "
        "For countries that don't have subdivisions, use None.",
    )

    return parser.parse_args()


def main() -> None:
    """
    Run the working days command-line application.

    Call the calculate function with the provided date
    and any optional command line arguments.

    Print the number of working days left in the month.
    Or, if arguments are invalid, display a helpful error message and exit.
    """

    # Enable colour formatting when application is bundled into an executable
    os.system("")  # nosec

    args = parse_arguments()

    try:
        result = calculate_working_days(args.date, args.country, args.subdiv)
    except ValueError:
        print(
            f"\n'{args.date}' is not a valid date. The format should be DD/MM/YYYY.\n"
            "Please correct the issue and try again.\n"
        )
        sys.exit()
    except NotImplementedError as ex:
        print(f"\nError: {ex}. " "Please correct the issue and try again.\n")
        if args.subdiv == SUBDIV:
            print(
                f"Note that {COUNTRY} is the default country "
                f"and {SUBDIV} is the default subdivision.\n"
                f"So if you choose a different country "
                "you also need to choose an associated subdivision.\n"
                "Or, if the selected country doesn't have subdivisions, use None.\n"
            )
        sys.exit()

    print()
    print(colored(figlet_format("Working Days"), color="green"))
    print(colored("Created for Gosia by Jon.\n", color="green"))

    print(
        "The remaining number of working days in the month after "
        f"{args.date} is {result}.\n"
    )
    print(f"The country used for this calculation was {args.country}.")
    if args.subdiv != "None":
        print(f"And the subdivision was {args.subdiv}.")
    print()


if __name__ == "__main__":
    main()
