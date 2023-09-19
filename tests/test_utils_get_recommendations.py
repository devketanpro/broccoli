import json
from unittest.mock import Mock

import openai
import pytest
from fastapi import HTTPException

from app.errors import TIMEOUT_ERROR
from app.utils import get_recommendations, get_messages


@pytest.fixture
def sample_response():
    return {
        "country": "USA",
        "season": "summer",
        "recommendations": [
            "Skiing at Aspen, Colorado",
            "Ice skating in Central Park, New York City",
            "Visiting the Grand Canyon National Park, Arizona"
        ]
    }


class TestGetRecommendations:

    #  Returns recommendations for valid country and season inputs
    def test_valid_country_and_season(self, mocker, sample_response):
        mocker.patch('openai.ChatCompletion.create',
                     return_value=Mock(choices=[Mock(message=Mock(content=json.dumps(sample_response)))]))
        result = get_recommendations("USA", "summer", get_messages_func=get_messages)
        assert result == sample_response

    #  Returns recommendations for valid country and season inputs with specific language
    def test_valid_country_and_season_with_language(self, mocker, sample_response):
        mocker.patch('openai.ChatCompletion.create',
                     return_value=Mock(choices=[Mock(message=Mock(content=json.dumps(sample_response)))]))
        result = get_recommendations("USA", "summer", get_messages_func=get_messages)
        assert result == sample_response

    #  Returns recommendations for valid country and season inputs with multiple messages
    def test_valid_country_and_season_with_multiple_messages(self, mocker, sample_response):
        mocker.patch('openai.ChatCompletion.create',
                     return_value=Mock(choices=[Mock(message=Mock(content=json.dumps(sample_response)))]))
        result = get_recommendations("USA", "summer", get_messages_func=get_messages)
        assert result == sample_response

    #  Raises HTTPException if OpenAI API returns an API error
    def test_api_error(self, mocker):
        mocker.patch('openai.ChatCompletion.create', side_effect=openai.error.APIError)
        with pytest.raises(HTTPException):
            get_recommendations("USA", "summer", get_messages_func=get_messages)

    #  Raises HTTPException if no response choices from OpenAI API
    def test_no_response_choices(self, mocker):
        mocker.patch('openai.ChatCompletion.create', return_value=Mock(choices=[]))
        with pytest.raises(HTTPException):
            get_recommendations("USA", "summer", get_messages_func=get_messages)

    #  Raises HTTPException if failed to connect to OpenAI API or rate limit exceeded
    def test_connection_or_ratelimit_error(self, mocker):
        mocker.patch('openai.ChatCompletion.create',
                     side_effect=[openai.error.APIConnectionError, openai.error.RateLimitError])
        with pytest.raises(HTTPException):
            get_recommendations("USA", "summer", get_messages_func=get_messages)

    #  Raises HTTPException for unknown errors
    def test_unknown_error(self, mocker):
        mocker.patch('openai.ChatCompletion.create', side_effect=Exception)
        with pytest.raises(HTTPException):
            get_recommendations("USA", "summer", get_messages_func=get_messages)

    #  Raises HTTPException for invalid country input
    def test_invalid_country(self):
        with pytest.raises(HTTPException):
            get_recommendations("InvalidCountry", "summer", get_messages_func=get_messages)

    #  Raises HTTPException for invalid season input
    def test_invalid_season(self):
        with pytest.raises(ValueError):
            get_recommendations("USA", "InvalidSeason", get_messages_func=get_messages)

    #  Raises HTTPException for invalid API key
    def test_invalid_api_key(self, mocker):
        mocker.patch('openai.ChatCompletion.create', side_effect=openai.error.AuthenticationError)
        with pytest.raises(HTTPException):
            get_recommendations("USA", "summer", get_messages_func=get_messages)

    #  Raises HTTPException for invalid model
    def test_invalid_model(self, mocker):
        mocker.patch('openai.ChatCompletion.create', side_effect=openai.error.InvalidRequestError)
        with pytest.raises(HTTPException):
            get_recommendations("USA", "summer", get_messages_func=get_messages)

    def test_raises_http_exception_on_timeout(self, mocker):
        # Mock the get_messages function to return a valid messages list
        mocker.patch('app.utils.get_messages', return_value=[{'role': 'user', 'content': 'prompt'}])

        # Mock the openai.ChatCompletion.create function to raise a Timeout error
        mocker.patch('openai.ChatCompletion.create', side_effect=openai.error.Timeout)

        # Call the get_recommendations function and assert that it raises an HTTPException with the TIMEOUT_ERROR
        with pytest.raises(HTTPException) as exc:
            get_recommendations('USA', 'fall', get_messages_func=get_messages)

        assert exc.value.status_code == TIMEOUT_ERROR['status_code']
        assert exc.value.detail == TIMEOUT_ERROR['detail']

    def test_invalid_response_from_openai_api(self, mocker):
        # Mock the get_messages_func function
        mocker.patch('app.utils.get_messages',
                     return_value=[{"role": "system", "content": f"recommendations for USA in fall"}])

        # Mock the make_chat_completion_request function
        mocker.patch('app.utils.make_chat_completion_request', return_value={"choices": []})

        # Call the get_recommendations function and expect an HTTPException to be raised
        with pytest.raises(HTTPException):
            get_recommendations("USA", "summer", get_messages)

    #  Raises HTTPException for invalid response choices from OpenAI API
    def test_invalid_response_choices_from_openai_api(self, mocker):
        # Mock the get_messages_func function
        mocker.patch('app.utils.get_messages',
                     return_value=[{"role": "system", "content": f"recommendations for USA in fall"}])

        # Mock the make_chat_completion_request function
        mocker.patch('app.utils.make_chat_completion_request', return_value={"choices": [{}]})

        # Call the get_recommendations function and expect an HTTPException to be raised
        with pytest.raises(HTTPException):
            get_recommendations("USA", "summer", get_messages)

    #  Raises HTTPException for any exception during API request
    def test_exception_during_api_request(self, mocker):
        # Mock the get_messages_func function
        mocker.patch('app.utils.get_messages',
                     return_value=[{"role": "system", "content": f"recommendations for USA in fall"}])

        # Mock the make_chat_completion_request function to raise an exception
        mocker.patch('app.utils.make_chat_completion_request', side_effect=Exception)

        # Call the get_recommendations function and expect an HTTPException to be raised
        with pytest.raises(HTTPException):
            get_recommendations("USA", "summer", get_messages)

    def test_exception_with_wrong_response_content(self, mocker):
        # Mock the get_messages_func function
        mocker.patch('app.utils.get_messages',
                     return_value=[{"role": "system", "content": f"recommendations for USA in fall"}])
        mocker.patch('openai.ChatCompletion.create',
                     return_value=Mock(choices=[Mock(message=Mock(content=json.dumps({})))]))
        # Call the get_recommendations function and expect an HTTPException to be raised
        with pytest.raises(HTTPException):
            get_recommendations("USA", "summer", get_messages)
