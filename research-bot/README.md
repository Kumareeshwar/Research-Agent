# Research Bot

A multi-agent system that researches questions on the web. Send a question to a Telegram bot (e.g. *"Which storm made landfall in Odisha this week?"*) and get back a short answer with the source URLs it used.

> Built to answer one question reliably: **what do current sources actually say?**

## How it works

```
You (Telegram)
   -> bots/telegram_bot.py   long-polls Telegram, forwards the message
   -> api/main.py            FastAPI: POST /ask
   -> graph/workflow.py      LangGraph workflow
        planner              turns the question into 3 search queries
        researcher           runs each query on Tavily
        writer               short answer + source URLs
   -> answer returned -> bot sends it to your chat
```

All agents share one LangGraph `State` object (question, queries, results, answer). Agents never call each other directly.

## Agents and tools

| Component | Role |
|---|---|
| Planner | Turns the question into targeted search queries |
| Researcher | Runs every query and collects the results |
| Writer | Summarizes the results into the final answer |
| `search_web` (Tavily) | Returns titles, URLs and content snippets |

The answer is written **only from retrieved sources**, never from the model's memory.

## Harness

| Layer | Implementation |
|---|---|
| Orchestration | LangGraph (planner -> researcher -> writer) |
| State | Shared typed `State` |
| LLM | Groq (`openai/gpt-oss-120b` by default) |
| Tracing | LangSmith |
| Evals | DeepEval (answer relevancy, faithfulness) with a Groq judge |
| Tests | pytest |

## Evaluation results

Eval set: 3 recent news questions (`evals/test_research_quality.py`), both metrics with a 0.7 threshold.

| Version | Answer relevancy | Faithfulness |
|---|---|---|
| Baseline | TBD | TBD |

## Project structure

```
research-bot/
├── agents/         # planner, researcher, writer
├── graph/          # LangGraph wiring
├── tools/          # search_web
├── api/            # FastAPI app
├── bots/           # Telegram bot
├── tests/          # unit tests
├── evals/          # DeepEval tests + Groq judge
└── config.py       # loads .env, creates the shared LLM
```

## Setup

```bash
git clone <repo-url> && cd research-bot
pip install -r requirements.txt
cp .env.example .env     # fill in keys
```

`.env`:

```
TELEGRAM_BOT_TOKEN=      # from @BotFather
GROQ_API_KEY=
TAVILY_API_KEY=
GROQ_MODEL=openai/gpt-oss-120b
API_URL=http://127.0.0.1:8000
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=research-bot
```

## Run

```bash
uvicorn api.main:app --reload     # terminal 1
python -m bots.telegram_bot       # terminal 2
```

Then message your bot on Telegram.

## Test and evaluate

```bash
pytest tests/
deepeval test run evals/test_research_quality.py   # calls live Groq + Tavily
```
