import json
from typing import List, Dict, Any

import openai
from fastapi import HTTPException

from app.constants import API_KEY, PROMPT, MODEL
from app.errors import RESPONSE_ERROR, API_ERROR, CONNECTION_OR_RATELIMIT_ERROR, UNKNOWN_ERROR


def get_messages(country: str, season: str) -> List[Dict[str, str]]:
    if not country or not season:
        return []

    if not isinstance(country, str) or not isinstance(season, str):
        raise TypeError

    prompt = PROMPT.format(country=country, season=season)
    return [{'role': 'user', 'content': f'{prompt}'}]


def get_recommendations(country: str, season: str) -> Dict[str, Any]:
    # Generate the prompt with specific language if mentioned
    messages = get_messages(country=country, season=season)

    try:
        # Make a request to the OpenAI API
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            api_key=API_KEY,
        )

        # Check if there are response choices
        if response.choices:
            return json.loads(response.choices[0].message.content)
        else:
            raise HTTPException(**RESPONSE_ERROR)

    except openai.error.APIError:
        raise HTTPException(**API_ERROR)

    except (openai.error.APIConnectionError, openai.error.RateLimitError):
        raise HTTPException(**CONNECTION_OR_RATELIMIT_ERROR)

    except Exception:
        raise HTTPException(**UNKNOWN_ERROR)
