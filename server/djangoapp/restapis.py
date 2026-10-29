import os
import logging

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

# Seconds to wait for the other services before giving up
TIMEOUT = 15


def get_request(endpoint, **kwargs):
    """GET `backend_url + endpoint`; keyword arguments become the query
    string. Returns the decoded JSON, or None if the call failed."""
    request_url = backend_url + endpoint
    try:
        response = requests.get(request_url, params=kwargs, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as err:
        logger.error("GET %s failed: %s", request_url, err)
        return None


def analyze_review_sentiments(text):
    """Ask the sentiment microservice to classify `text`.
    Returns the JSON ({"sentiment": ...}) or None on failure."""
    request_url = sentiment_analyzer_url.rstrip('/') + "/analyze/"
    try:
        # requests percent-encodes the text so spaces/punctuation are safe
        response = requests.get(request_url + requests.utils.quote(
            text, safe=''), timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as err:
        logger.error("Sentiment analysis failed: %s", err)
        return None


def post_review(data_dict):
    """Send a new review to the Express API. Returns the saved review
    (JSON) or None on failure."""
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(
            request_url, json=data_dict, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError) as err:
        logger.error("POST %s failed: %s", request_url, err)
        return None
