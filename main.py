from fastapi import FastAPI
from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("Server running and connected to Supabase")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)