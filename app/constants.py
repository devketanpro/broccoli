SEASONS = ["summer", "spring", "fall", "winter"]
API_KEY = "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"
MODEL = "gpt-3.5-turbo"
PROMPT = (
    "Generate a personalized travel itinerary for a trip to {country}. "
    "The traveler is interested in a vacation during {season}. "
    "including suggested activity options for one place"
    "Convert all details into a JSON response with keys country, season and recommendations list."
    "Provide short and quick response in three lines"
)
MESSAGE = {'role': 'user', 'content': '{prompt}'}

