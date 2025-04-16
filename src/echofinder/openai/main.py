from openai import OpenAI

from src.echofinder.constants import OPENAI_API_KEY

if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=OPENAI_API_KEY)
