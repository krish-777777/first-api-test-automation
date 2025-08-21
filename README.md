# AI-Powered API Test Automation Example (Gemini-1.5-flash)

A simple, end-to-end example that demonstrates **agents** for:
- CRUD operations against a demo FastAPI service
- AI-driven test data generation
- Structured logging to files
- Optional integration with **Gemini-1.5-flash** (uses the Google `genai` client)

> ✅ Runs fully offline with a deterministic fallback if you don't set an API key.

---

## Project layout

```
ai_api_test_automation_example/
├── ai/
│   ├── agents.py            # TestDataAgent, CRUDTestAgent, LoggingAgent
│   └── gemini_client.py     # Wrapper for Gemini-1.5-flash with graceful fallback
├── app/
│   └── server.py            # FastAPI demo app (CRUD on /items)
├── framework/
│   ├── config.py            # Config & env loading
│   ├── http_client.py       # Thin wrapper around requests with logging
│   └── logger.py            # Logging setup
├── tests/
│   ├── run_tests.py         # Orchestrates agents end-to-end
│   └── schemas.py           # Pydantic schema for validation
├── quickstart.py            # One-shot: start server + run agents/tests
├── requirements.txt
├── .env.template
└── README.md
```

## Requirements

- Python 3.10+
- (Optional) Google Gemini API key for live AI: set `GOOGLE_API_KEY`

Install deps:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.template .env       # and edit if you have an API key
```

## Run the demo

**Option A: One command (auto-start server & run AI agents)**

```bash
python quickstart.py
```

**Option B: Manual steps**

Terminal 1 – start the app:
```bash
uvicorn app.server:app --host 127.0.0.1 --port 8000 --reload
```

Terminal 2 – run the AI agents/tests:
```bash
python tests/run_tests.py
```

Logs are written to `logs/app.log` (server) and `logs/tests.log` (test run).

## What the agents do

- **LoggingAgent**: configures file+console logging.
- **TestDataAgent**: *tries* Gemini-1.5-flash to craft diverse and edge-case payloads. If no key, uses a Faker-based generator + rule-based variations (nulls, long strings, etc.).
- **CRUDTestAgent**: plans a CRUD sequence (Create → Read → Update → Delete) and executes it via the `framework.http_client` with validations.

## Endpoints (FastAPI demo)

- `POST /items` – create item
- `GET /items/{item_id}` – get one
- `GET /items` – list items
- `PUT /items/{item_id}` – full update
- `PATCH /items/{item_id}` – partial update
- `DELETE /items/{item_id}` – delete

### Sample Item schema
```json
{
  "name": "string (1..100)",
  "price": "float > 0",
  "description": "string (optional, <= 500)",
  "tags": ["string", ...]    // optional, <= 10 items
}
```

## Using Gemini-1.5-flash

If you set `GOOGLE_API_KEY` in `.env`, the **TestDataAgent** will call Gemini-1.5-flash to generate test data variants:

- **Model**: `gemini-1.5-flash`
- **Library**: `google.genai` (new) or `google.generativeai` (compat). The wrapper picks what's available.

If there’s any import/auth failure, it falls back gracefully to the local generator so you can still run everything offline.

## Extending

- Swap the demo app with your real API by changing `BASE_URL` in `.env`.
- Add auth headers in `framework/http_client.py`.
- Teach the **CRUDTestAgent** to read an OpenAPI spec and ask the LLM to derive test plans.
- Emit JUnit XML or Allure results.

---

Happy testing!
