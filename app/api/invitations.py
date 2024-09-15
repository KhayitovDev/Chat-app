from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from uuid import UUID

from app.services.utils import get_current_user_from_request
from app.services import crud, schemas
from app.db.database import get_db

router = APIRouter()


@router.post("/invitation")
def create_invitaion(invitation: schemas.InvitationCreate, db: Session=Depends(get_db), current_user: dict = Depends(get_current_user_from_request)):
    invitation = crud.send_invitation(
        db, 
        invitation
        )
    return invitation


@router.post("/invitations/{invitation_id}/status/")
def update_invitation_status_endpoint(
    invitation_id: UUID, 
    status_update: schemas.InvitationStatusUpdate, 
    db: Session = Depends(get_db)
):
    invitation = crud.accept_invitation(db, invitation_id)
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    
    invitation.status = status_update.status
    db.commit()
    db.refresh(invitation)
    
    return invitation