import pytest
from fastapi import HTTPException

from app.constants import PROMPT
from app.utils import get_messages


class TestGetMessages:

    #  Returns a list of messages when valid country and season are provided.
    def test_valid_country_and_season(self):
        country = "United States"
        season = "summer"
        expected_messages = [
            {"role": "user", "content": PROMPT.format(country=country, season=season)}
        ]
        assert get_messages(country, season) == expected_messages

    #  Returns a list with a single message when country or season is missing.
    def test_missing_country_or_season(self):
        country = "USA"
        season = ""
        expected_messages = [{"role": "user", "content": "Season is required."}]
        assert get_messages(country, season) == expected_messages

    #  Raises TypeError when country parameter is not a string.
    def test_invalid_country_type(self):
        country = 123
        season = "summer"
        with pytest.raises(HTTPException):
            get_messages(country, season)

    #  Raises TypeError when season parameter is not a string.
    def test_invalid_season_type(self):
        country = "USA"
        season = 123
        with pytest.raises(HTTPException):
            get_messages(country, season)

    #  Raises HTTPResponse when an invalid season is provided.
    def test_invalid_season_value(self):
        country = "USA"
        season = "summer2"
        with pytest.raises(HTTPException):
            get_messages(country, season)

    #  Returns a list of messages with the correct prompt when valid country and season are provided.
    def test_correct_prompt(self):
        country = "United States"
        season = "summer"
        expected_messages = [
            {"role": "user", "content": PROMPT.format(country=country, season=season)}
        ]
        assert get_messages(country, season) == expected_messages

    #  Returns a list with a single message when country parameter is an empty string.
    def test_empty_country(self):
        country = ""
        season = "summer"
        expected_messages = [{"role": "user", "content": "Country is required."}]
        assert get_messages(country, season) == expected_messages

    #  Returns a list with a single message when season parameter is an empty string.
    def test_empty_season(self):
        country = "USA"
        season = ""
        expected_messages = [{"role": "user", "content": "Season is required."}]
        assert get_messages(country, season) == expected_messages

    #  Returns a list with a single message when an invalid season is provided.
    def test_invalid_season(self):
        country = "USA"
        season = "summer2"
        with pytest.raises(HTTPException):
            get_messages(country, season)
