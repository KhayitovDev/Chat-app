from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services import crud, schemas
from app.db.database import get_db

from uuid import UUID

router = APIRouter()

@router.post("/messages/")
def send_message(
    message_create: schemas.MessageCreate,
    db: Session = Depends(get_db)
):
    message = crud.create_message(
        db, 
        message_create.sender_id, 
        message_create.receiver_id, 
        message_create.content
    )
    if message:
        return message
    else:
        raise HTTPException(status_code=400, detail="Failed to send message")
    
@router.get("/messages/")
def get_message_history(
    sender_id: UUID,
    receiver_id: UUID,
    db: Session = Depends(get_db)
):
    messages = crud.get_messages(db, sender_id, receiver_id)
    if messages:
        return messages
    else:
        raise HTTPException(status_code=404, detail="No messages found")