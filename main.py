from fastapi import FastAPI, HTTPException, Response
from dotenv import load_dotenv
import os
from supabase import create_client
from pydantic import BaseModel

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("Server running and connected to Supabase")


# Pydantic models for request body validation
class SignupRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@app.post("/auth/signup")
async def signup(request: SignupRequest):
    email = request.email.strip() if request.email else ""
    password = request.password.strip() if request.password else ""

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    try:
        response = supabase_client.auth.sign_up({"email": email, "password": password})
        # Return the user object from Supabase response with 201 status
        return Response({"user": response.user}, status_code=201)
    except Exception as e:
        # Return Supabase error message
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auth/login")
async def login(request: LoginRequest):
    email = request.email.strip() if request.email else ""
    password = request.password.strip() if request.password else ""

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    try:
        response = supabase_client.auth.sign_in_with_password({"email": email, "password": password})
        session = response.session
        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid login credentials")


@app.get("/public/info")
async def public_info():
    return {"message": "Welcome stranger! This info is public."}


@app.get("/protected/profile")
async def protected_profile(authorization: str = None):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Access token required")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Access token required")
    token = authorization[len("Bearer "):]
    try:
        # Supabase auth.get_user(access_token) validates the Bearer token
        # Returns structure varies by SDK version - commonly {"user": User, "session": Session} dict,
        # or just the User object directly. We handle both patterns.
        sup_response = supabase_client.auth.get_user(token)
        # Normalize to access the user object
        if hasattr(sup_response, "user"):
            user = sup_response.user  # Pattern: sup_response = {"user": user_obj, ...}
        elif isinstance(sup_response, dict) and "user" in sup_response:
            user = sup_response["user"]  # Dict pattern
        else:
            user = sup_response  # Assume direct User object
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        # Return user profile data - assuming User has: id, email, created_at attributes
        return {
            "id": user.id,
            "email": user.email,
            "created_at": user.created_at,
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)