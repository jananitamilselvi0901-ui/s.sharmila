from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    description="AI-powered educational learning assistant",
    version="1.0.0"
)


# -----------------------------
# Static files
# -----------------------------

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


# -----------------------------
# Templates
# -----------------------------

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


# -----------------------------
# Request Models
# -----------------------------

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )


class QuizRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )

    question_count: int = Field(
        default=3,
        ge=1,
        le=10
    )


# -----------------------------
# Home Page
# -----------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "EduGenie"
    }


# -----------------------------
# Q&A
# -----------------------------

@app.post("/qa")
async def qa(payload: TextRequest):

    result = answer_question(
        payload.text
    )

    return {
        "result": result
    }


# -----------------------------
# Explanation
# -----------------------------

@app.post("/explain")
async def explain(payload: TextRequest):

    result = explain_topic(
        payload.text
    )

    return {
        "result": result
    }


# -----------------------------
# Quiz
# -----------------------------

@app.post("/quiz")
async def quiz(payload: QuizRequest):

    questions = generate_quiz(
        payload.text,
        payload.question_count
    )

    return {
        "questions": questions
    }


# -----------------------------
# Summary
# -----------------------------

@app.post("/summarize")
async def summarize(payload: TextRequest):

    result = summarize_text(
        payload.text
    )

    return {
        "result": result
    }


# -----------------------------
# Learning Path
# -----------------------------

@app.post("/learn/recommendations")
async def learning_recommendations(
    payload: TextRequest
):

    result = get_learning_recommendations(
        payload.text
    )

    return {
        "result": result
    }


# -----------------------------
# API Information
# -----------------------------

@app.get("/api")
async def api_info():

    return {
        "name": "EduGenie API",
        "endpoints": [
            "/qa",
            "/explain",
            "/quiz",
            "/summarize",
            "/learn/recommendations"
        ]
    }