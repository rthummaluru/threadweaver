from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ProjectRequest(BaseModel):
    project_name: str
    team_emails: list[str] = []
    

@app.post("/create-ecosystem")
async def create_ecosystem(data: ProjectRequest):
    print("Creating ecosystem for project: ", data.project_name)
    print("Inviting: ", data.team_emails)
    return {"status": "success", "project": data.project_name}