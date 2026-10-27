# FastAPI Calculator

![Tests](https://github.com/hptankeu1/fastapi-calculator/actions/workflows/tests.yml/badge.svg)

A small web calculator built with FastAPI, tested at three levels (unit, integration, end-to-end with Playwright), with structured logging and continuous integration through GitHub Actions.

## Project structure

```
fastapi-calculator/
├── app/
│   ├── logging_config.py        # Console + rotating file logging (logs/app.log)
│   └── operations/__init__.py   # add, subtract, multiply, divide
├── templates/index.html         # Calculator web page
├── main.py                      # FastAPI app and API endpoints
├── tests/
│   ├── conftest.py              # Starts the live server for E2E tests
│   ├── unit/                    # Tests for app/operations
│   ├── integration/             # Tests for every endpoint in main.py
│   └── e2e/                     # Playwright browser tests
├── .github/workflows/tests.yml  # CI: runs all tests on every push
├── pytest.ini
└── requirements.txt
```

## Setup

```bash
git clone https://github.com/hptankeu1/fastapi-calculator.git
cd fastapi-calculator
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

## Run the application

```bash
python main.py
# or
uvicorn main:app --reload
```

Open http://127.0.0.1:8000 in your browser. Interactive API docs are at http://127.0.0.1:8000/docs.

## API endpoints

| Method | Path        | Body                 | Response                      |
|--------|-------------|----------------------|-------------------------------|
| GET    | `/`         | —                    | Calculator page               |
| GET    | `/health`   | —                    | `{"status": "ok"}`            |
| POST   | `/add`      | `{"a": 10, "b": 5}`  | `{"result": 15}`              |
| POST   | `/subtract` | `{"a": 10, "b": 5}`  | `{"result": 5}`               |
| POST   | `/multiply` | `{"a": 10, "b": 5}`  | `{"result": 50}`              |
| POST   | `/divide`   | `{"a": 10, "b": 5}`  | `{"result": 2}`               |

Errors (division by zero, missing or non-numeric values) return HTTP 400 with `{"error": "..."}`.

## Run the tests

```bash
pytest                                  # everything
pytest tests/unit --cov=app             # unit tests with coverage
pytest tests/integration                # API endpoint tests
pytest tests/e2e --browser chromium     # Playwright browser tests
pytest tests/e2e --headed               # watch the browser while testing
```

## Logging

Logging is configured in `app/logging_config.py`:

- Every HTTP request and response status is logged by a middleware.
- Every calculation and its result is logged; errors (division by zero, invalid input) are logged at `ERROR` level.
- Output goes to the console and to `logs/app.log` (rotating, 1 MB × 3 files).
- Set the console level with `LOG_LEVEL=DEBUG uvicorn main:app`.

Example log lines:

```
2026-10-26 21:43:19 | INFO     | calculator | Request: POST /multiply
2026-10-26 21:43:19 | INFO     | calculator | multiply(12.0, 4.0) = 48.0
2026-10-26 21:43:19 | INFO     | calculator | Response: POST /multiply -> 200
```

## Continuous integration

`.github/workflows/tests.yml` runs on every push and pull request: it installs dependencies and Chromium, then runs the unit, integration and end-to-end suites as separate steps.
