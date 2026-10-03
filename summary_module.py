import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_summary(text: str):
    prompt = f"""
Summarize the following educational paragraph.

Requirements:
- Give 5 to 6 important points.
- Keep each point short and clear.
- Use simple language.
- Include only the important information.

Educational paragraph:
{text}
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text