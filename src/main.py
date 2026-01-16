from fastapi import FastAPI, Request
from src.agent.loop import reviewPR
from src.agent.tools import getDiff, postPR

app = FastAPI()

@app.post("/webhook")
async def recieve_webhook(request: Request):
    body = await request.json()
    action = body["action"]
    if action == "opened" or action == "reopened":
        diffUrl = body["pull_request"]["diff_url"]
        diff  = getDiff(diffUrl)
        result = reviewPR(diff)
        if result:
            postPR(body["pull_request"]["number"], result) 

    # print(body)
    return {"recieved":True}

@app.get("/")
async def root():
    return {"message": "Hello World"}