import calendar
import datetime
import holidays


def calculate_working_days(start_date: str) -> int:

    start_date = datetime.datetime.strptime(start_date, "%d/%m/%Y")
    year = start_date.year
    month = start_date.month
    first_day = start_date.day
    
    bank_holidays = holidays.UK(subdiv='England', years=year)
    month_length = calendar.monthrange(year, month)[1]

    working_days = 0

    for day in range(first_day, month_length + 1):
        
        weekday = calendar.weekday(year, month, day)
        date = datetime.date(year, month, day)

        if weekday < 5 and date not in bank_holidays:
            working_days += 1
    
    return working_days


if __name__=="__main__":
    print(calculate_working_days("03/05/1985"))
