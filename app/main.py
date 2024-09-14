

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import users, invitations, message

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(invitations.router, prefix="/api/invitations", tags=["invitations"])
app.include_router(message.router, prefix="/api/messages", tags=["messages"])
