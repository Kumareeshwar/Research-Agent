# FastAPI server. The Telegram bot sends questions here.
from fastapi import FastAPI
from pydantic import BaseModel

from graph.workflow import graph

app = FastAPI()


class Question(BaseModel):
    question: str


@app.post("/ask")
def ask(body: Question):
    result = graph.invoke({"question": body.question})
    return {"answer": result["answer"]}
