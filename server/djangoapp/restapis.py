# import os, requests
# from dotenv import load_dotenv

# load_dotenv()
# backend_url = (os.getenv("backend_url") or "").rstrip("/")

# def get_request(endpoint, **kwargs):
#     url = f"{backend_url}{endpoint}"
#     try:
#         # requests will add the query string from kwargs safely
#         r = requests.get(url, params=kwargs, timeout=10)
#         r.raise_for_status()
#         return r.json()
#     except Exception as e:
#         print(f"[get_request] error calling {url}: {e}")
#         return []  # return an empty list instead of None




# def analyze_review_sentiments(text):
#     request_url = sentiment_analyzer_url+"analyze/"+text
#     try:
#         # Call get method of requests library with URL and parameters
#         response = requests.get(request_url)
#         return response.json()
#     except Exception as err:
#         print(f"Unexpected {err=}, {type(err)=}")
#         print("Network exception occurred")


# server/djangoapp/restapis.py
import os, requests
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

backend_url = (os.getenv("backend_url") or "").rstrip("/")
sentiment_analyzer_url = (os.getenv("sentiment_analyzer_url") or "").rstrip("/")

def get_request(endpoint, **kwargs):
    url = f"{backend_url}{endpoint}"
    try:
        r = requests.get(url, params=kwargs, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[get_request] error calling {url}: {e}")
        return []

def analyze_review_sentiments(text: str) -> str:
    """Return 'positive' | 'neutral' | 'negative' (default neutral on error)."""
    if not text:
        return "neutral"
    if not sentiment_analyzer_url:
        # No env var set; don’t break the page
        return "neutral"

    url = f"{sentiment_analyzer_url}/analyze/{quote_plus(text)}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # adapt this line to your service's response shape if needed
        return (data.get("label") or data.get("sentiment") or "neutral").lower()
    except Exception as e:
        print(f"[sentiment] error calling {url}: {e}")
        return "neutral"

def post_review(data_dict):
    url = f"{backend_url}/insert_review"
    try:
        r = requests.post(url, json=data_dict, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"[post_review] error calling {url}: {e}")
        return {"error": str(e)}