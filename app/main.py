from typing import Union, Dict, Any

from fastapi import FastAPI, HTTPException

from app.constants import SEASONS
from app.errors import SEASON_ERROR
from app.utils import get_recommendations

app = FastAPI()


@app.get("/")
async def travel_recommendation(country: str, season: str) -> Union[Dict[str, Any], Dict[str, Union[str, Any]]]:
    # Check if seasons are valid
    if season not in SEASONS:
        raise HTTPException(**SEASON_ERROR)

    return get_recommendations(country=country, season=season)

