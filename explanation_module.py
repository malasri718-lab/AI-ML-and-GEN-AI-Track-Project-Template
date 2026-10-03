import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def explain_concept(question: str) -> str:

    prompt = f"""
Explain the following concept for a beginner student.

Concept:
{question}

Requirements:
- Use very simple English.
- Give a clear definition.
- Explain in a beginner-friendly way.
- Give 2 or 3 simple examples.
- Avoid difficult technical words.
- Keep the answer concise.
"""

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=prompt
    )

    return response.text