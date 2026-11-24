
# import os
# from dotenv import load_dotenv
# from google import genai

# load_dotenv()

# API_KEY = os.getenv("GEMINI_API_KEY")
# MODEL = os.getenv("GEMINI_MODEL")

# if not API_KEY:
#     raise ValueError("GEMINI_API_KEY is missing in .env")

# if not MODEL:
#     raise ValueError("GEMINI_MODEL is missing in .env")

# client = genai.Client(api_key=API_KEY)


# def ask_gemini(prompt):

#     response = client.models.generate_content(
#         model=MODEL,
#         contents=prompt
#     )

#     return response.text

# print(ask_gemini("Hi, How are you?"))


import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError, ClientError

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env")

if not MODEL:
    raise ValueError("GEMINI_MODEL is missing in .env")

client = genai.Client(api_key=API_KEY)


def ask_gemini(prompt, max_retries=4):

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )

            return response.text

        except (ServerError, ClientError) as error:

            # Retry temporary server and rate-limit errors
            status_code = getattr(error, "code", None)

            if status_code not in (429, 500, 502, 503, 504):
                raise

            if attempt == max_retries - 1:
                print("Gemini failed after all retry attempts.")
                raise

            wait_time = 2 ** (attempt + 1)

            print(
                f"Gemini API error ({status_code}). "
                f"Attempt {attempt + 1}/{max_retries}. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)

        except (ConnectionError, TimeoutError, OSError) as error:

            if attempt == max_retries - 1:
                print("Connection failed after all retry attempts.")
                raise

            wait_time = 2 ** (attempt + 1)

            print(
                f"Connection error: {error}. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print(ask_gemini("Hi, how are you?"))
