import pytest
from fastapi.exceptions import HTTPException

from app.main import travel_recommendation


@pytest.fixture
def recommendations():
    return {
        "country": "USA",
        "season": "Summer",
        "recommendations": [
            "Visit New York City and explore iconic landmarks like Times Square and Central Park.",
            "Experience the stunning natural beauty of Yosemite National Park through hiking and camping.",
            "Relax on the sunny beaches of Miami and enjoy water sports like swimming and snorkeling."
        ]
    }


class TestTravelRecommendation:

    #  Valid country and season inputs return recommendations
    @pytest.mark.asyncio
    async def test_valid_country_and_season(self, mocker, recommendations):
        # Mock the get_recommendations function
        mocker.patch('app.main.get_recommendations', return_value=recommendations)

        # Call the travel_recommendation function with valid inputs
        response = await travel_recommendation('USA', 'summer')

        # Check if the response contains the expected recommendations
        assert response == recommendations

    #  Valid country and default season (summer) return recommendations
    @pytest.mark.asyncio
    async def test_valid_country_and_default_season(self, mocker, recommendations):
        # Mock the get_recommendations function
        mocker.patch('app.main.get_recommendations', return_value=recommendations)
        # Call the travel_recommendation function with valid country and default season
        with pytest.raises(HTTPException) as exc_info:
            await travel_recommendation('USA', '')

        # Check if the response contains the expected recommendations
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == 'Invalid season. Please choose from spring, summer, fall, or winter.'

    #  Valid country and season with special characters return recommendations
    @pytest.mark.asyncio
    async def test_valid_country_and_season_with_special_characters(self, mocker, recommendations):
        # Mock the get_recommendations function
        mocker.patch('app.main.get_recommendations', return_value=recommendations)

        # Call the travel_recommendation function with valid country and season with special characters
        with pytest.raises(HTTPException) as exc_info:
            await travel_recommendation('USA', 'summer!')

        # Check if the response contains the expected recommendations
        assert exc_info.value.status_code == 400
        assert exc_info.value.detail == 'Invalid season. Please choose from spring, summer, fall, or winter.'

    #  Invalid country input raises HTTPException
    @pytest.mark.asyncio
    async def test_invalid_country_input(self, mocker):
        # Call the travel_recommendation function with invalid country input
        with pytest.raises(HTTPException):
            await travel_recommendation('', 'summer')

    #  Invalid season input raises HTTPException
    @pytest.mark.asyncio
    async def test_invalid_season_input(self, mocker):
        # Call the travel_recommendation function with invalid season input
        with pytest.raises(HTTPException):
            await travel_recommendation('USA', 'autumn')

    #  Empty country input raises HTTPException
    @pytest.mark.asyncio
    async def test_empty_country_input(self, mocker):
        # Call the travel_recommendation function with empty country input
        with pytest.raises(HTTPException):
            await travel_recommendation('', 'summer')
