import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"


def call_llm(prompt):
    """
    Send prompt to LLM and return response
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    result = response.json()

    return result["response"]


def build_prompt(task, html, knowledge, memory):
    """
    Construct the agent prompt
    """

    prompt = f"""
You are an AI web automation agent.

Your job is to complete tasks by controlling a browser.

Available actions:

navigate(url)
click(selector)
type(selector,value)
read_html()
read_memory(key)
write_memory(key,value)
search_knowledge(query)
ask_user(question)

Return ONLY valid JSON.

Example:

{{
 "action":"click",
 "selector":"#next"
}}

Current task:
{task}

Relevant knowledge:
{knowledge}

Stored memory:
{memory}

Current webpage HTML snippet:
{html}

Decide the next action.
"""

    return prompt


def get_next_action(task, html, knowledge, memory):
    """
    Generate next action from LLM
    """

    prompt = build_prompt(task, html, knowledge, memory)

    response = call_llm(prompt)

    try:
        action = json.loads(response)
        return action
    except:
        return {
            "action": "error",
            "message": response
        }
