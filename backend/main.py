from fastapi import FastAPI
from pydantic import BaseModel
from backend.agent_controller import run_agent

app = FastAPI()


class TaskRequest(BaseModel):
    task: str
    user_id: str = "user1"


@app.get("/")
def root():
    return {"message": "AI Agent Backend Running"}


@app.post("/run-agent")
def start_agent(request: TaskRequest):
    """
    Start the automation agent
    """

    result = run_agent(
        task=request.task,
        user_id=request.user_id
    )

    return result
