import pytest

import context
from workingdays import calculate_working_days


def test_calculate_working_days():
    start_day = 3
    month_length = 31
    total_days = month_length - (start_day - 1)
    weekend_days = 8
    bank_holidays = 2
    expected = total_days - weekend_days - bank_holidays

    result = calculate_working_days("03/05/1985")

    assert result == expected


if __name__ == "__main__":
    pytest.main()
