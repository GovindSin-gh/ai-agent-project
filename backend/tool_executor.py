import requests

from memory.redis_client import get_value, set_value
from rag.vectordb import search


PUPPETEER_URL = "http://localhost:3000"


def navigate(url):
    """
    Open webpage
    """
    r = requests.post(
        f"{PUPPETEER_URL}/navigate",
        json={"url": url}
    )
    return r.json()


def click(selector):
    """
    Click element
    """
    r = requests.post(
        f"{PUPPETEER_URL}/click",
        json={"selector": selector}
    )
    return r.json()


def type_text(selector, value):
    """
    Type text into input
    """
    r = requests.post(
        f"{PUPPETEER_URL}/type",
        json={
            "selector": selector,
            "value": value
        }
    )
    return r.json()


def get_html():
    """
    Get page HTML
    """
    r = requests.get(f"{PUPPETEER_URL}/html")
    return r.json()


def read_memory(key):
    """
    Read value from Redis
    """
    return get_value(key)


def write_memory(key, value):
    """
    Write value to Redis
    """
    set_value(key, value)
    return {"status": "stored"}


def search_knowledge(query):
    """
    Search vector database
    """
    return search(query)


def execute_tool(action):
    """
    Main tool dispatcher
    """

    tool = action.get("action")

    if tool == "navigate":
        return navigate(action["url"])

    elif tool == "click":
        return click(action["selector"])

    elif tool == "type":
        return type_text(action["selector"], action["value"])

    elif tool == "read_html":
        return get_html()

    elif tool == "read_memory":
        return read_memory(action["key"])

    elif tool == "write_memory":
        return write_memory(action["key"], action["value"])

    elif tool == "search_knowledge":
        return search_knowledge(action["query"])

    else:
        return {"error": "Unknown action"}
