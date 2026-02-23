from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm


from sqlalchemy.orm import Session
from jose import JWTError, jwt

from db.session import get_db
from models.user import User
from schemas.user import UserCreate, UserLogin
from utils.security import hash_password, verify_password
from utils.jwt_handler import create_access_token
from core.config import settings


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# This enables Swagger Authorize button
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# -----------------------------
# REGISTER
# -----------------------------
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


# -----------------------------
# LOGIN
# -----------------------------
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user or not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": db_user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# -----------------------------
# GET CURRENT USER
# -----------------------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return email

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# -----------------------------
# PROTECTED ROUTE
# -----------------------------
@router.get("/me")
def read_users_me(current_user: str = Depends(get_current_user)):
    return {"email": current_user}