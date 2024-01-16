import requests

from reykunyu_py.util import Response


def request(input_text: str) -> Response:
    """Get the response from the Reykunyu API for a particular Na'vi string."""
    return Response(input_text, requests.get("https://reykunyu.wimiso.nl/api/fwew?t%C3%ACpawm=" + input_text).json())

# def dictionary() -> Dictionary:
#     """Get the full list of words used by Reykunyu."""
#     return Dictionary(requests.get("https://reykunyu.wimiso.nl/api/frau").json())