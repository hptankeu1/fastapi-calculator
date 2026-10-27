"""End-to-end tests: Playwright drives a real browser against the running app."""

import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.e2e


def _calculate(page: Page, base_url: str, a: str, b: str, button: str):
    page.goto(base_url)
    page.fill("#a", a)
    page.fill("#b", b)
    page.click(f'button[aria-label="{button}"]')


def test_page_loads(page: Page, fastapi_server):
    page.goto(fastapi_server)
    expect(page).to_have_title("FastAPI Calculator")
    expect(page.locator("h1")).to_have_text("FastAPI Calculator")


@pytest.mark.parametrize(
    "a, b, button, expected",
    [
        ("10", "5", "Add", "Calculation Result: 15"),
        ("10", "5", "Subtract", "Calculation Result: 5"),
        ("10", "5", "Multiply", "Calculation Result: 50"),
        ("10", "4", "Divide", "Calculation Result: 2.5"),
        ("-3", "1.5", "Add", "Calculation Result: -1.5"),
    ],
)
def test_operations_in_browser(page: Page, fastapi_server, a, b, button, expected):
    _calculate(page, fastapi_server, a, b, button)
    expect(page.locator("#result")).to_have_text(expected)


def test_divide_by_zero_shows_error(page: Page, fastapi_server):
    _calculate(page, fastapi_server, "10", "0", "Divide")
    expect(page.locator("#result")).to_have_text("Error: Cannot divide by zero!")


def test_empty_input_shows_error(page: Page, fastapi_server):
    page.goto(fastapi_server)
    page.fill("#a", "7")
    page.click('button[aria-label="Add"]')
    expect(page.locator("#result")).to_have_text("Error: Please enter both numbers.")
