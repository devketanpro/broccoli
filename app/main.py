from typing import Union, Dict, Any

from fastapi import FastAPI, HTTPException

from app.constants import SEASONS
from app.errors import SEASON_ERROR
from app.utils import get_recommendations, get_messages

app = FastAPI()


@app.get("/")
async def travel_recommendation(country: str, season: str) -> Union[Dict[str, Any], Dict[str, Union[str, Any]]]:
    """
    Provides travel recommendations based on the given country and season.

    Args:
        country (str): The name of the country for which travel recommendations are requested.
        season (str): The season for which travel recommendations are requested.

    Returns:
        Union[Dict[str, Any], Dict[str, Union[str, Any]]]: A dictionary containing travel recommendations.
        The structure of the dictionary depends on the specific implementation of `get_recommendations` function.

    Raises:
        HTTPException: If the provided season is not valid.

    """
    # Check if seasons are valid
    if season not in SEASONS:
        raise HTTPException(**SEASON_ERROR)
    return get_recommendations(country=country, season=season, get_messages_func=get_messages)
