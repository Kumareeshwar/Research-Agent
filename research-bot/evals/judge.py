# DeepEval judge model. DeepEval defaults to OpenAI, so we point it at the same Groq LLM.
import os

from deepeval.models import DeepEvalBaseLLM
from langchain_groq import ChatGroq

import config  # noqa: F401  (loads .env)

# Own client so we can retry harder: Groq's free tier caps tokens per minute (429s).
judge_llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
    temperature=0,
    max_retries=10,
)


class GroqJudge(DeepEvalBaseLLM):
    def __init__(self):
        pass

    def load_model(self):
        return judge_llm

    def generate(self, prompt: str, schema=None):
        if schema is not None:
            structured = self.load_model().with_structured_output(schema, method="json_schema")
            return structured.invoke(prompt)
        return self.load_model().invoke(prompt).content

    async def a_generate(self, prompt: str, schema=None):
        if schema is not None:
            structured = self.load_model().with_structured_output(schema, method="json_schema")
            return await structured.ainvoke(prompt)
        return (await self.load_model().ainvoke(prompt)).content

    def get_model_name(self):
        return "groq-judge"
