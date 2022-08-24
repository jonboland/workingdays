import pytest
from argparse import Namespace

from workingdays import calculate


def test_calculate_working_days_May_1985_England():
    given_day = 3
    month_length = 31
    total_days = month_length - given_day
    weekend_days = 8
    bank_holidays = 2
    expected = total_days - weekend_days - bank_holidays

    result = calculate.calculate_working_days("03/05/1985")

    assert result == expected


@pytest.mark.parametrize(
    "date, expected",
    [
        ("02/02/2022", 18),
        ("12/04/2022", 11),
        ("21/06/2022", 7),
        ("01/08/2022", 21),
        ("13/10/2022", 12),
        ("20/12/2022", 6),
    ],
)
def test_calculate_working_days_2022_England(date, expected):

    result = calculate.calculate_working_days(date)

    assert result == expected


@pytest.mark.parametrize(
    "date, expected",
    [
        ("09/01/2030", 16),
        ("06/04/2033", 15),
        ("18/05/2034", 8),
        ("01/09/2037", 21),
        ("12/11/2038", 12),
        ("27/12/2039", 3),
    ],
)
def test_calculate_working_days_2030s_England(date, expected):

    result = calculate.calculate_working_days(date)

    assert result == expected


@pytest.mark.parametrize(
    "date, expected, subdiv",
    [("01/01/2023", 21, "England"), ("01/01/2023", 20, "Scotland")],
)
def test_calculate_working_days_Jan_England_Scotland(date, expected, subdiv):

    result = calculate.calculate_working_days(date, subdiv=subdiv)

    assert result == expected


@pytest.mark.parametrize(
    "country, subdiv, expected",
    [("Australia", "NSW", 20), ("US", "NY", 21), ("Turkey", "None", 22)],
)
def test_calculate_working_days_other_countries(country, subdiv, expected):

    result = calculate.calculate_working_days("01/12/2024", country, subdiv)

    assert result == expected


def test_calculate_working_days_leap_year_2028_England():
    expected = 11

    result = calculate.calculate_working_days("14/02/2028")

    assert result == expected


def test_main_valid_args_correct_output_displayed(monkeypatch, capsys):
    def fake_args():
        return Namespace(date="06/04/2023", country="GB", subdiv="England")

    monkeypatch.setattr(calculate, "parse_arguments", fake_args)

    expected = (
        "\nThe remaining number of working days in the month after 06/04/2023 is 14.\n\n"
        "The country used for this calculation was GB.\n"
        "And the subdivision was England.\n\n"
    )

    calculate.main()
    captured = capsys.readouterr()
    # Slice removes figlet and intro text
    result = captured.out[436:]

    assert result == expected


def test_main_invalid_date(monkeypatch, capsys):
    def fake_args():
        return Namespace(date="55/04/2023", country="GB", subdiv="England")

    monkeypatch.setattr(calculate, "parse_arguments", fake_args)

    expected = (
        "\n'55/04/2023' is not a valid date. The format should be DD/MM/YYYY.\n"
        "Please correct the issue and try again.\n\n"
    )

    with pytest.raises(SystemExit):
        calculate.main()

    captured = capsys.readouterr()
    result = captured.out

    assert result == expected


def test_main_unavailable_country(monkeypatch, capsys):
    def fake_args():
        return Namespace(date="01/02/1999", country="Atlantis", subdiv="None")

    monkeypatch.setattr(calculate, "parse_arguments", fake_args)

    expected = "\nError: Country Atlantis not available. Please correct the issue and try again.\n\n"

    with pytest.raises(SystemExit):
        calculate.main()

    captured = capsys.readouterr()
    result = captured.out

    assert result == expected


def test_main_non_default_country_subdiv_not_changed(monkeypatch, capsys):
    def fake_args():
        return Namespace(date="01/02/1999", country="US", subdiv="England")

    monkeypatch.setattr(calculate, "parse_arguments", fake_args)

    expected = (
        "\nError: Country US does not have subdivision 'England'. "
        "Please correct the issue and try again.\n\n"
        "Note that GB is the default country and England is the default subdivision.\n"
        "So if you choose a different country you also need to choose "
        "an associated subdivision.\n"
        "Or, if the selected country doesn't have subdivisions, use None.\n\n"
    )

    with pytest.raises(SystemExit):
        calculate.main()

    captured = capsys.readouterr()
    result = captured.out

    assert result == expected


if __name__ == "__main__":
    pytest.main()
