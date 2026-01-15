from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/webhook")
async def recieve_webhook(request: Request):
    body = await request.json()
    action = body["action"]
    if action == "opened" or action == "reopened":
        diffUrl = body["pull_request"]["diff_url"]
        print(diffUrl)

    # print(body)
    return {"recieved":True}

@app.get("/")
async def root():
    return {"message": "Hello World"}