from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from models.organization import Organization
from api.auth import get_current_user

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("/")
def create_organization(
    name: str,
    db: Session = Depends(get_db)
):

    org = Organization(name=name)

    db.add(org)
    db.commit()
    db.refresh(org)

    return org