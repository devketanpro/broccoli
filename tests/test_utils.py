import json
from unittest.mock import Mock

import openai
import pytest
from fastapi import HTTPException

from app.errors import TIMEOUT_ERROR
from app.utils import get_recommendations, get_messages


class TestGetMessages:

    #  Returns a list with one dictionary containing the user message.
    def test_returns_list_with_one_dictionary_containing_user_message(self):
        result = get_messages("USA", "summer")
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], dict)
        assert result[0]["role"] == "user"
        assert ("Generate a personalized travel itinerary for a trip to USA. The traveler is interested in a vacation "
                "during summer. including suggested activity options for one placeConvert all details into a JSON "
                "response with keys country, season and recommendations list.Provide short and quick response in "
                "three lines") in result[0]["content"]

    #  Returns a list with one dictionary containing the user message with the correct country and season.
    def test_returns_list_with_one_dictionary_containing_user_message_with_correct_country_and_season(self):
        result = get_messages("France", "spring")
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], dict)
        assert result[0]["role"] == "user"
        assert ("Generate a personalized travel itinerary for a trip to France. The traveler is interested in a "
                "vacation during spring. including suggested activity options for one placeConvert all details into a "
                "JSON response with keys country, season and recommendations list.Provide short and quick response in "
                "three lines") in result[0]["content"]

    #  Returns an empty list when country and season are empty strings.
    def test_returns_empty_list_when_country_and_season_are_empty_strings(self):
        result = get_messages("", "")
        assert isinstance(result, list)
        assert len(result) == 0

    #  Returns an empty list when country and season are None.
    def test_returns_empty_list_when_country_and_season_are_none(self):
        result = get_messages(None, None)
        assert isinstance(result, list)
        assert len(result) == 0

    #  Raises a TypeError when country or season are not strings.
    def test_raises_type_error_when_country_or_season_are_not_strings(self):
        with pytest.raises(TypeError):
            get_messages(123, "summer")
        with pytest.raises(TypeError):
            get_messages("USA", 456)

    #  Returns a list with one dictionary containing the user message with special characters in the country and season.
    def test_returns_list_with_one_dictionary_containing_user_message_with_special_characters_in_country_and_season(
            self):
        result = get_messages("Côte d'Ivoire", "été")
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], dict)
        assert result[0]["role"] == "user"
        assert ("Generate a personalized travel itinerary for a trip to Côte d'Ivoire. The traveler is interested in a "
                "vacation during été. including suggested activity options for one placeConvert all details into a "
                "JSON response with keys country, season and recommendations list.Provide short and quick response in "
                "three lines") in \
               result[0]["content"]

    #  Returns a list with one dictionary containing the user message with a long country and season.
    def test_returns_list_with_one_dictionary_containing_user_message_with_long_country_and_season(self):
        result = get_messages("United States of America", "spring")
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], dict)
        assert result[0]["role"] == "user"
        assert ("Generate a personalized travel itinerary for a trip to United States of America. The traveler is "
                "interested in a vacation during spring. including suggested activity options for one placeConvert "
                "all details into a JSON response with keys country, season and recommendations list.Provide short "
                "and quick response in three lines") in \
               result[0]["content"]

    #  Returns a list with one dictionary containing the user message with a short country and season.
    def test_returns_list_with_one_dictionary_containing_user_message_with_short_country_and_season(self):
        result = get_messages("UK", "fall")
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], dict)
        assert result[0]["role"] == "user"
        assert ("Generate a personalized travel itinerary for a trip to UK. The traveler is interested in a vacation "
                "during fall. including suggested activity options for one placeConvert all details into a JSON "
                "response with keys country, season and recommendations list.Provide short and quick response in "
                "three lines") in \
               result[0]["content"]

    #  Returns a list with one dictionary containing the user message with a country and season that have numbers.
    def test_returns_list_with_one_dictionary_containing_user_message_with_country_and_season_that_have_numbers(self):
        result = get_messages("USA123", "2022")
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], dict)
        assert result[0]["role"] == "user"
        assert ("Generate a personalized travel itinerary for a trip to USA123. The traveler is interested in a "
                "vacation during 2022. including suggested activity options for one placeConvert all details into a "
                "JSON response with keys country, season and recommendations list.Provide short and quick response in "
                "three lines") in \
               result[0]["content"]

    # Returns a list with one dictionary containing the user message with a country and season that have special
    # characters.
    def test_get_message_with_country_and_season_that_have_special_characters(self):
        result = get_messages("!@#$%^&*", "summer!")
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], dict)
        assert result[0]["role"] == "user"
        assert ("Generate a personalized travel itinerary for a trip to !@#$%^&*. The traveler is interested in a "
                "vacation during summer!. including suggested activity options for one placeConvert all details into "
                "a JSON response with keys country, season and recommendations list.Provide short and quick response "
                "in three lines") in \
               result[0]["content"]


class TestGetRecommendations:

    #  Returns recommendations for valid country and season inputs
    def test_valid_country_and_season(self, mocker):
        mocker.patch('openai.ChatCompletion.create',
                     return_value=Mock(choices=[Mock(message=Mock(content=json.dumps({"recommendation": "test"})))]))
        result = get_recommendations("USA", "summer")
        assert result == {"recommendation": "test"}

    #  Returns recommendations for valid country and season inputs with specific language
    def test_valid_country_and_season_with_language(self, mocker):
        mocker.patch('openai.ChatCompletion.create',
                     return_value=Mock(choices=[Mock(message=Mock(content=json.dumps({"recommendation": "test"})))]))
        result = get_recommendations("USA", "summer")
        assert result == {"recommendation": "test"}

    #  Returns recommendations for valid country and season inputs with multiple messages
    def test_valid_country_and_season_with_multiple_messages(self, mocker):
        mocker.patch('openai.ChatCompletion.create',
                     return_value=Mock(choices=[Mock(message=Mock(content=json.dumps({"recommendation": "test"})))]))
        result = get_recommendations("USA", "summer")
        assert result == {"recommendation": "test"}

    #  Raises HTTPException if OpenAI API returns an API error
    def test_api_error(self, mocker):
        mocker.patch('openai.ChatCompletion.create', side_effect=openai.error.APIError)
        with pytest.raises(HTTPException):
            get_recommendations("USA", "summer")

    #  Raises HTTPException if no response choices from OpenAI API
    def test_no_response_choices(self, mocker):
        mocker.patch('openai.ChatCompletion.create', return_value=Mock(choices=[]))
        with pytest.raises(HTTPException):
            get_recommendations("USA", "summer")

    #  Raises HTTPException if failed to connect to OpenAI API or rate limit exceeded
    def test_connection_or_ratelimit_error(self, mocker):
        mocker.patch('openai.ChatCompletion.create',
                     side_effect=[openai.error.APIConnectionError, openai.error.RateLimitError])
        with pytest.raises(HTTPException):
            get_recommendations("USA", "summer")

    #  Raises HTTPException for unknown errors
    def test_unknown_error(self, mocker):
        mocker.patch('openai.ChatCompletion.create', side_effect=Exception)
        with pytest.raises(HTTPException):
            get_recommendations("USA", "summer")

    #  Returns recommendations for valid country and season inputs with empty messages
    def test_empty_messages(self, mocker):
        mocker.patch('openai.ChatCompletion.create',
                     return_value=Mock(choices=[Mock(message=Mock(content=json.dumps({"recommendation": "test"})))]))
        result = get_recommendations("USA", "summer")
        assert result == {"recommendation": "test"}

    #  Raises HTTPException for invalid country input
    def test_invalid_country(self):
        with pytest.raises(HTTPException):
            get_recommendations("InvalidCountry", "summer")

    #  Raises HTTPException for invalid season input
    def test_invalid_season(self):
        with pytest.raises(HTTPException):
            get_recommendations("USA", "InvalidSeason")

    #  Raises HTTPException for invalid API key
    def test_invalid_api_key(self, mocker):
        mocker.patch('openai.ChatCompletion.create', side_effect=openai.error.AuthenticationError)
        with pytest.raises(HTTPException):
            get_recommendations("USA", "summer")

    #  Raises HTTPException for invalid model
    def test_invalid_model(self, mocker):
        mocker.patch('openai.ChatCompletion.create', side_effect=openai.error.InvalidRequestError)
        with pytest.raises(HTTPException):
            get_recommendations("USA", "summer")

    def test_raises_http_exception_on_timeout(self, mocker):
        # Mock the get_messages function to return a valid messages list
        mocker.patch('app.utils.get_messages', return_value=[{'role': 'user', 'content': 'prompt'}])

        # Mock the openai.ChatCompletion.create function to raise a Timeout error
        mocker.patch('openai.ChatCompletion.create', side_effect=openai.error.Timeout)

        # Call the get_recommendations function and assert that it raises an HTTPException with the TIMEOUT_ERROR
        with pytest.raises(HTTPException) as exc:
            get_recommendations('country', 'season')

        assert exc.value.status_code == TIMEOUT_ERROR['status_code']
        assert exc.value.detail == TIMEOUT_ERROR['detail']
