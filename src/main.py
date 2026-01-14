from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/webhook")
async def recieve_webhook(request: Request):
    body = await request.json()
    print(body)
    return {"recieved":True}

@app.get("/")
async def root():
    return {"message": "Hello World"}
