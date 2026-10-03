from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_quiz(topic):
    prompt = f"""
Create a quiz for the topic: {topic}

Requirements:
- Create exactly 3 multiple-choice questions.
- Each question must have exactly 4 options: A, B, C, D.
- Include the correct answer.
- Include a short explanation for the correct answer.

Return ONLY valid JSON in this format:

{{
    "questions": [
        {{
            "question": "Question 1",
            "options": {{
                "A": "Option A",
                "B": "Option B",
                "C": "Option C",
                "D": "Option D"
            }},
            "correct_answer": "B",
            "explanation": "Short explanation"
        }}
    ]
}}

Topic: {topic}
"""

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text[7:]

    if text.endswith("```"):
        text = text[:-3]

    return json.loads(text.strip())

def check_quiz(questions, user_answers):
    score = 0
    results = []

    for index, question in enumerate(questions):
        user_answer = user_answers[index]
        correct_answer = question["correct_answer"]

        if user_answer == correct_answer:
            score += 1
            results.append({
                "question": question["question"],
                "your_answer": user_answer,
                "correct": True
            })
        else:
            results.append({
                "question": question["question"],
                "your_answer": user_answer,
                "correct": False,
                "correct_answer": correct_answer,
                "explanation": question["explanation"]
            })

    return {
        "score": score,
        "total": len(questions),
        "results": results
    }

