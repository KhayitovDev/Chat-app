

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import Message, User
from app.services.schemas import MessageCreate
from app.services.translate import translate_text


from app.api import users, invitations, message

import json
from uuid import UUID

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

app.mount("/static", StaticFiles(directory="static/"), name="static")


app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(invitations.router, prefix="/api/invitations", tags=["invitations"])
app.include_router(message.router, prefix="/api/messages", tags=["messages"])


connections = {}




@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    try:
        user_id = UUID(user_id)  
    except ValueError:
        await websocket.close()
        return

    await websocket.accept()
    connections[user_id] = websocket  
    print(f"User {user_id} connected. Active connections: {list(connections.keys())}")

    db: Session = next(get_db())
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            receiver_id = UUID(message_data["receiver_id"])
            content = message_data["content"]

            if not receiver_id or not content:
                await websocket.send_text("Invalid message format")
                continue


            message_create = MessageCreate(sender_id=user_id, receiver_id=receiver_id, content=content)
            db_message = Message(**message_create.model_dump())
            db.add(db_message)
            db.commit()
            
            sender = db.query(User).filter_by(id=user_id).first()
            receiver = db.query(User).filter_by(id=receiver_id).first()
            
            sender_lang = sender.preferred_language
            receiver_lang = receiver.preferred_language
            
            if sender_lang and sender_lang != receiver_lang:
                try:

                    translated_message = translate_text(content, sender_lang, receiver_lang)
                except Exception as e:
                    print(f"Error translating message: {str(e)}")
                    translated_message = content  
            else:
                translated_message = content  
                
            # await websocket.send_text(f"{content}")
            
            if receiver_id in connections:
                await connections[receiver_id].send_text(f"{sender.username}: {translated_message}")
    
    except WebSocketDisconnect:
        del connections[user_id] 
        print(f"User {user_id} disconnected. Active connections: {list(connections.keys())}")
        
        
@app.get("/")
def get():
    return FileResponse("static/index.html")