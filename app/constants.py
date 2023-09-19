import os

import openai

from app.errors import API_ERROR, CONNECTION_OR_RATELIMIT_ERROR, TIMEOUT_ERROR

API_KEY = os.environ.get('API_KEY')
MODEL = os.environ.get("MODEL")

SEASONS = ["summer", "spring", "fall", "winter"]
PROMPT = (
    "Generate a personalized travel itinerary for a trip to {country}. "
    "The traveler is interested in a vacation during {season}. "
    "including suggested activity options for one place"
    "Convert all details into a JSON response with keys country, season and recommendations list."
    "Provide short and quick response in three lines"
)
MESSAGE = {'role': 'user', 'content': '{prompt}'}
API_TIMEOUT = 5
EXCEPTION_MAPPING = {
    openai.error.APIError: API_ERROR,
    openai.error.APIConnectionError: CONNECTION_OR_RATELIMIT_ERROR,
    openai.error.RateLimitError: CONNECTION_OR_RATELIMIT_ERROR,
    openai.error.Timeout: TIMEOUT_ERROR
}
