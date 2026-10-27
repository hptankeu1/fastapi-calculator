"""Shared fixtures: starts the real FastAPI server for the E2E tests."""

import os
import subprocess
import sys
import time

import pytest
import requests

BASE_URL = "http://127.0.0.1:8001"


@pytest.fixture(scope="session")
def fastapi_server():
    """Run uvicorn in a subprocess for the whole test session, then stop it."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8001"],
        cwd=project_root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # Wait up to 30 seconds for the server to answer.
    deadline = time.time() + 30
    while time.time() < deadline:
        try:
            if requests.get(f"{BASE_URL}/health", timeout=1).status_code == 200:
                break
        except requests.ConnectionError:
            time.sleep(0.5)
    else:
        process.terminate()
        raise RuntimeError("FastAPI server did not start in time")

    yield BASE_URL

    process.terminate()
    process.wait(timeout=10)
