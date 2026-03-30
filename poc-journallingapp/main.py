import fastapi as fastapi
from dotenv import load_dotenv
import kiteconnect as kiteconnect
import os

from db import close_mongodb_connection, connect_to_mongodb

load_dotenv()
app = fastapi.FastAPI()
kite= kiteconnect.KiteConnect(api_key=os.getenv("KITE_API_KEY"))


# @app.on_event("startup")
# def startup_event():
#     connect_to_mongodb()


# @app.on_event("shutdown")
# def shutdown_event():
#     close_mongodb_connection()

@app.get("/login")
def login():
    return {"login_url": kite.login_url()}

@app.get("/auth/callback")
def auth_callback(request_token: str):
    data=kite.generate_session(request_token, api_secret=os.getenv("KITE_API_SECRET"))
    kite.set_access_token(data["access_token"])
    return {"message": "Authentication successful", "data": data}

@app.get("/trades")
def get_trades():
    return {"trades": kite.trades()}

# @app.get("/")
# def handle_redirect(request_token: str, action: str):
#     """This endpoint receives the redirect from Zerodha with the request_token"""
#     return {
#         "message": "You have been redirected from Zerodha",
#         "request_token": request_token,
#         "action": action,
#         "next_step": f"Call /auth/callback?request_token={request_token}"
#     }