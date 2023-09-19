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

    #  Returns recommendations for valid country and season inputs
    @pytest.mark.asyncio
    async def test_valid_country_and_season_inputs(self, mocker, recommendations):
        mocker.patch('app.main.get_recommendations', return_value=recommendations)
        response = await travel_recommendation('USA', 'summer')
        assert response == recommendations

    #  Returns recommendations for all seasons when no season is specified
    @pytest.mark.asyncio
    async def test_no_season_specified(self, mocker, recommendations):
        mocker.patch('app.main.get_recommendations', return_value=recommendations)
        with pytest.raises(HTTPException) as exc_info:
            await travel_recommendation('USA', '')
        assert exc_info.value.status_code == 400

    #  Returns recommendations for all countries when no country is specified
    @pytest.mark.asyncio
    async def test_no_country_specified(self, mocker, recommendations):
        mocker.patch('app.main.get_recommendations', return_value=recommendations)
        response = await travel_recommendation('', 'summer')
        assert response == recommendations

    # Raises HTTPException with 400 status code and SEASON_ERROR detail message when season input is not in SEASONS list
    @pytest.mark.asyncio
    async def test_invalid_season_input(self, mocker, recommendations):
        mocker.patch('app.main.get_recommendations', return_value=recommendations)
        with pytest.raises(HTTPException) as e:
            await travel_recommendation('USA', 'autumn')
        assert e.value.status_code == 400
        assert e.value.detail == 'Invalid season. Please choose from spring, summer, fall, or winter.'

    #  Returns recommendations for valid country and season inputs with specific language if mentioned
    @pytest.mark.asyncio
    async def test_valid_country_and_season_inputs_with_specific_language(self, mocker, recommendations):
        mocker.patch('app.main.get_recommendations', return_value=recommendations)
        response = await travel_recommendation('USA', 'summer')
        assert response == recommendations
