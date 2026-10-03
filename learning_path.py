import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_learning_path(topic: str):

    prompt = f"""
Create a clear learning path for a student who wants to learn {topic}.

Divide the learning path into exactly 3 levels:

Level 1 – Beginner
Level 2 – Intermediate
Level 3 – Advanced

For each level, provide important topics to learn.

Also provide:
- Recommended Videos
- Recommended Articles
- Recommended Books
- Practice suggestions

Keep the explanation simple and student-friendly.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text