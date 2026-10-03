from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from qna import ask_gemini
from explanation_module import explain_concept
from quiz_module import generate_quiz, check_quiz
from summary_module import generate_summary
from learning_path import generate_learning_path

app = FastAPI(title="EduGenie API")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class UserInput(BaseModel):
    text: str
class QuizInput(BaseModel):
    topic: str
class QuizQuestion(BaseModel):
    question: str
    options: dict
    correct_answer: str
    explanation: str


class QuizAnswerInput(BaseModel):
    questions: list[QuizQuestion]
    answers: list[str]

class LearningPathInput(BaseModel):
    topic: str

class GenerateInput(BaseModel):
    task: str
    question: str

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/qa")
def question_answer(data: UserInput):
    answer = ask_gemini(data.text)

    return {
        "endpoint": "/qa",
        "question": data.text,
        "answer": answer
    }


@app.post("/explain")
def explain(data: UserInput):
    answer = explain_concept(data.text)

    return {
        "endpoint": "/explain",
        "question": data.text,
        "answer": answer
    }


@app.post("/quiz")
def create_quiz(data: QuizInput):
    quiz = generate_quiz(data.topic)

    return quiz

@app.post("/quiz/result")
def quiz_result(data: QuizAnswerInput):
    result = check_quiz(
        [question.model_dump() for question in data.questions],
        data.answers
    )

    return result


@app.post("/summary")
def summary(data: UserInput):
    result = generate_summary(data.text)

    return {
        "endpoint": "/summary",
        "question": data.text,
        "summary": result
    }


@app.post("/learning-path")
def learning_path(data: LearningPathInput):

    result = generate_learning_path(data.topic)

    return {
        "topic": data.topic,
        "learning_path": result
    }



@app.post("/generate")
def generate(data: GenerateInput):

    try:
        if data.task == "explain":
            result = explain_concept(data.question)

        elif data.task == "qa":
            result = ask_gemini(data.question)

        elif data.task == "summary":
            result = generate_summary(data.question)

        elif data.task == "learning_path":
            result = generate_learning_path(data.question)

        else:
            result = "Quiz is handled separately."

        return {
            "response": result
        }

    except Exception:
        return {
            "response": "⚠️ Unable to generate a response right now. Please try again in a few seconds."
        }