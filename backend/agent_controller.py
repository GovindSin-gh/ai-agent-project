from backend.llm_engine import get_next_action
from backend.tool_executor import execute_tool
from rag.vectordb import search
from memory.redis_client import get_user_data

MAX_STEPS = 15


def run_agent(task, user_id="user1"):
    """
    Main agent execution loop
    """

    # retrieve stored memory
    memory = get_user_data(user_id)

    # retrieve knowledge for task
    knowledge = search(task)

    html = ""

    step = 0

    while step < MAX_STEPS:

        print(f"\n--- Step {step+1} ---")

        # Ask LLM for next action
        action = get_next_action(
            task=task,
            html=html,
            knowledge=knowledge,
            memory=memory
        )

        print("LLM Action:", action)

        if action.get("action") == "finish":
            return {"status": "completed", "message": "Task finished"}

        if action.get("action") == "ask_user":
            return {
                "status": "waiting_for_user",
                "question": action.get("question")
            }

        # Execute tool
        result = execute_tool(action)

        print("Tool Result:", result)

        # If browser action, fetch updated HTML
        if action.get("action") in [
            "navigate",
            "click",
            "type"
        ]:
            html_response = execute_tool({"action": "read_html"})

            html = html_response.get("html", "")[:4000]

        step += 1

    return {
        "status": "failed",
        "message": "Max steps reached"
    }
