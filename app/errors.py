RESPONSE_ERROR = {"status_code": 400, "detail": "No response choices from OpenAI API"}
API_ERROR = {"status_code": 401, "detail": "OpenAI API returned an API Error"}
CONNECTION_OR_RATELIMIT_ERROR = {"status_code": 400, "detail": "Failed to connect to OpenAI API or rate limit exceeded"}
UNKNOWN_ERROR = {"status_code": 400, "detail": "Unknown error: please contact support"}
SEASON_ERROR = {"status_code": 400, "detail": "Invalid season. Please choose from spring, summer, fall, or winter."}
