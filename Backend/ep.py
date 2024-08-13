from fastapi import FastAPI, File, UploadFile, Request
import os
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from ap import main

app = FastAPI()

class Item(BaseModel):
    query:str

origins = [
    "http://localhost:5173",  # React app running on localhost
    "https://your-frontend-domain.com",  # Replace with your frontend domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],   # Allows all headers
)

@app.post("/upload")
async def upload_file(request: Request):
    try:
        form = await request.form()
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    print(form)
    file = form['file']  # Get the file
    query = form['description']  # Get the text description
    # file_content = await request.body()  # Read raw binary data

    print(file.decode(),query)
    # result=chat(query,file)

@app.post("/query")
async def query(request:Item):
    body=request
    print(body.dict())
    result=main(body.query)
    return JSONResponse(result)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)