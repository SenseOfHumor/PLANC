from google import genai
from pydantic import BaseModel
from core import utils

GEMINI_API_KEY = utils.get_gemini_api_key()
TEST_MODEL = "gemini-2.0-flash-lite"
PARSE_MODEL = "gemini-2.0-flash"

class Test(BaseModel):
    response: str

def test_gemini():
    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model= TEST_MODEL,
        contents="This is a test for response, Please respond with \"Up and running\"",
        config={
            "response_mime_type": "application/json",
            "response_schema": list[Test],
        },
    )
    # Use the response as a JSON string.
    # print(response.text)

    # Use instantiated objects.
    test_response : list[Test] = response.parsed
    if not test_response:
        raise ValueError("No response received from Gemini API.")
    return test_response[0].response

