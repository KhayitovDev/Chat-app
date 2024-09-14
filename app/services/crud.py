
from fastapi import HTTPException
from sqlalchemy.orm import Session

from uuid import UUID

from .bcrypt import hash_password
from .schemas import UserCreate, InvitationCreate, InvitationStatus, MessageCreate
from app.models.models import User, Invitation, Message

def create_user(db: Session, user: UserCreate):
    user_hash_password = hash_password(user.hashed_password)
    
    db_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        preferred_language=user.preferred_language,
        status=user.status,
        hashed_password=user_hash_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def send_invitation(db: Session, invitation:InvitationCreate):
    sender = db.query(User).filter(User.id == invitation.sender_id).first()
    receiver = db.query(User).filter(User.id == invitation.receiver_id).first()
    
    if not sender or not receiver:
        raise HTTPException(status_code=404, detail="Sender or receiver not found")
    
    db_invitation = Invitation(
        sender_id = invitation.sender_id,
        receiver_id=invitation.receiver_id,
        status=invitation.status
    )
    db.add(db_invitation)
    db.commit()
    db.refresh(db_invitation)
    return db_invitation

def accept_invitation(db: Session, invitation_id: UUID):
    invitation = db.query(Invitation).filter(Invitation.id == invitation_id).first()
    if invitation:
        invitation.status = InvitationStatus.ACCEPTED
        db.commit()
        db.refresh(invitation)
        return invitation
    return None


def create_message(db: Session, sender_id: UUID, receiver_id: UUID, content: str):
    message = Message(
        sender_id=sender_id,
        receiver_id=receiver_id,
        content=content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def get_messages(db:Session, sender_id: UUID, receiver_id: UUID):
    messages = db.query(Message).filter(
        (Message.sender_id == sender_id and Message.receiver_id == receiver_id) |
        (Message.sender_id == receiver_id and Message.receiver_id == sender_id)
    ).all()
    return messages
    