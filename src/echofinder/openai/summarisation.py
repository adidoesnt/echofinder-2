from src.echofinder.openai.main import client
from src.echofinder.constants import SUMMARISATION_MODEL

def get_prompt_response(prompt: str):
    response = client.chat.completions.create(
        model=SUMMARISATION_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    
    return response.choices[0].message.content
