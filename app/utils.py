import logging
from typing import List, Dict, Any, Callable

import openai
import pycountry
import ujson
from fastapi import HTTPException

from app.constants import API_KEY, PROMPT, MODEL, API_TIMEOUT, SEASONS, EXCEPTION_MAPPING
from app.errors import RESPONSE_ERROR, UNKNOWN_ERROR

ROLE_KEY = 'role'
CONTENT_KEY = 'content'


def get_messages(country: str, season: str) -> List[Dict[str, str]]:
    """
    Generate a list of messages for the chatbot.
    
    Args:
        country (str): The country for the travel itinerary.
        season (str): The season for the travel itinerary.
    
    Returns:
        List[Dict[str, str]]: A list of messages for the chatbot.
    """
    try:
        if not isinstance(country, str):
            raise TypeError("The 'country' parameter must be a string.")
        if not isinstance(season, str):
            raise TypeError("The 'season' parameter must be a string.")

        if not country:
            return [{ROLE_KEY: 'user', CONTENT_KEY: 'Country is required.'}]

        if not season:
            return [{ROLE_KEY: 'user', CONTENT_KEY: 'Season is required.'}]

        is_country_valid = pycountry.countries.get(name=country)
        if is_country_valid is None:
            raise ValueError("Invalid country.")

        if season not in SEASONS:
            raise ValueError("Invalid season.")
    except Exception as e:
        handle_error(e)

    prompt = PROMPT.format(country=country, season=season)
    return [{ROLE_KEY: 'user', CONTENT_KEY: f'{prompt}'}]


def validate_response(response: Dict) -> bool:
    if "country" in response and "season" in response and "recommendations" in response:
        if len(response["recommendations"]) == 3:
            return True
    return False


def get_recommendations(
        country: str,
        season: str,
        get_messages_func: Callable[[str, str], List[Dict[str, str]]]
) -> Dict[str, Any]:
    """
    Get recommendations based on country and season.
    
    Args:
        country (str): The country.
        season (str): The season.
        get_messages_func (Callable[[str, str], List[Dict[str, str]]]): Function to get messages.
    
    Returns:
        Dict[str, Any]: The recommendations.
    """
    # Generate the prompt with specific language if mentioned
    messages = get_messages_func(country, season)
    try:
        response = make_chat_completion_request(messages)
        if not response.choices:
            raise HTTPException(**RESPONSE_ERROR)

        result = ujson.loads(response.choices[0].message.content)
        if not validate_response(result):
            raise HTTPException(**RESPONSE_ERROR)

        return result
    except Exception as e:
        handle_error(e)


def make_chat_completion_request(messages: List[Dict[str, str]]) -> Any:
    """
    Make a request to the OpenAI API with a timeout.
    
    Args:
        messages (List[Dict[str, str]]): The messages.
    
    Returns:
        Any: The API response.
    """
    return openai.ChatCompletion.create(
        model=MODEL,
        messages=messages,
        api_key=API_KEY,
        timeout=API_TIMEOUT,
    )


def handle_error(exception):
    """
    Handle different types of exceptions in a centralized manner.
    
    Args:
        exception: The exception to handle.
    """
    logging.error(f"An error occurred: {exception}")

    exception_type = type(exception)
    if exception_type in EXCEPTION_MAPPING:
        raise HTTPException(**EXCEPTION_MAPPING[exception_type])
    elif error := exception.args:
        raise HTTPException(status_code=400, detail=error)
    else:
        raise HTTPException(**UNKNOWN_ERROR)
