from app.utils import validate_response


class TestValidateResponse:

    #  Valid response with country, season, and 3 recommendations
    def test_valid_response_with_country_season_and_3_recommendations(self):
        response = {
            "country": "USA",
            "season": "summer",
            "recommendations": ["beach", "hiking", "barbecue"]
        }
        assert validate_response(response) is True

    #  Valid response with additional fields and 3 recommendations
    def test_valid_response_with_additional_fields_and_3_recommendations(self):
        response = {
            "country": "USA",
            "season": "summer",
            "recommendations": ["beach", "hiking", "barbecue"],
            "temperature": "hot",
            "activities": ["swimming", "camping"]
        }
        assert validate_response(response) is True

    #  Valid response with country, season, and more than 3 recommendations
    def test_valid_response_with_country_season_and_more_than_3_recommendations(self):
        response = {
            "country": "USA",
            "season": "summer",
            "recommendations": ["beach", "hiking", "barbecue", "swimming"]
        }
        assert validate_response(response) is False

    #  Empty response
    def test_empty_response(self):
        response = {}
        assert validate_response(response) is False

    #  Response missing 'country' field
    def test_response_missing_country_field(self):
        response = {
            "season": "summer",
            "recommendations": ["beach", "hiking", "barbecue"]
        }
        assert validate_response(response) is False

    #  Response missing 'season' field
    def test_response_missing_season_field(self):
        response = {
            "country": "USA",
            "recommendations": ["beach", "hiking", "barbecue"]
        }
        assert validate_response(response) is False

    #  Response missing 'recommendations' field
    def test_response_missing_recommendations_field(self):
        response = {
            "country": "USA",
            "season": "summer"
        }
        assert validate_response(response) is False

    #  Response with less than 3 recommendations
    def test_response_with_less_than_3_recommendations(self):
        response = {
            "country": "USA",
            "season": "summer",
            "recommendations": ["beach", "hiking"]
        }
        assert validate_response(response) is False

    #  Response with more than 3 recommendations
    def test_response_with_more_than_3_recommendations(self):
        response = {
            "country": "USA",
            "season": "summer",
            "recommendations": ["beach", "hiking", "barbecue", "swimming", "camping"]
        }
        assert validate_response(response) is False

    #  Response with empty recommendations list
    def test_response_with_empty_recommendations_list(self):
        response = {
            "country": "USA",
            "season": "summer",
            "recommendations": []
        }
        assert validate_response(response) is False
