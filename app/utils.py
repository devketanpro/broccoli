from typing import List, Dict, Any

import openai
import ujson
from fastapi import HTTPException

from app.constants import API_KEY, PROMPT, MODEL, API_TIMEOUT, SEASONS
from app.errors import RESPONSE_ERROR, API_ERROR, CONNECTION_OR_RATELIMIT_ERROR, UNKNOWN_ERROR, TIMEOUT_ERROR

PROMPT = "Please enter your {country} and {season}."

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
    if not isinstance(country, str):
        raise TypeError("The 'country' parameter must be a string.")
    if not isinstance(season, str):
        raise TypeError("The 'season' parameter must be a string.")

    if not country:
        return [{ROLE_KEY: 'user', CONTENT_KEY: 'Country is required.'}]

    if not season:
        return [{ROLE_KEY: 'user', CONTENT_KEY: 'Season is required.'}]

    if season not in SEASONS:
        raise ValueError("Invalid season.")

    prompt = PROMPT.format(country=country, season=season)
    return [{ROLE_KEY: 'user', CONTENT_KEY: f'{prompt}'}]


def get_recommendations(country: str, season: str) -> Dict[str, Any]:
    # Generate the prompt with specific language if mentioned
    messages = get_messages(country=country, season=season)
    try:
        # Make a request to the OpenAI API with a timeout
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            api_key=API_KEY,
            timeout=API_TIMEOUT,  # Set a timeout value in seconds
        )
        # Check if there are response choices
        if response.choices:
            return ujson.loads(response.choices[0].message.content)
        else:
            raise HTTPException(**RESPONSE_ERROR)
    except openai.error.APIError:
        raise HTTPException(**API_ERROR)
    except (openai.error.APIConnectionError, openai.error.RateLimitError):
        raise HTTPException(**CONNECTION_OR_RATELIMIT_ERROR)
    except openai.error.Timeout:
        raise HTTPException(**TIMEOUT_ERROR)
    except Exception:
        raise HTTPException(**UNKNOWN_ERROR)
