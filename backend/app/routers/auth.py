from datetime import time as time_type

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: schemas.UserRegister, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists")

    if payload.role == models.UserRole.organization and not payload.organization_name:
        raise HTTPException(status_code=400, detail="organization_name is required when registering as an organization")

    user = models.User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.flush()  # get user.id before commit

    if payload.role == models.UserRole.organization:
        org = models.Organization(
            owner_id=user.id,
            name=payload.organization_name,
            domain=payload.domain or "General",
            address=payload.address,
            working_hours=payload.working_hours or "09:00 AM - 05:00 PM",
        )
        db.add(org)

    db.commit()
    db.refresh(user)

    access_token = create_access_token(data={"sub": user.id, "role": user.role.value})
    return schemas.TokenResponse(access_token=access_token, user=schemas.UserOut.model_validate(user))


@router.post("/login", response_model=schemas.TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.id, "role": user.role.value})
    return schemas.TokenResponse(access_token=access_token, user=schemas.UserOut.model_validate(user))


@router.post("/login-json", response_model=schemas.TokenResponse)
def login_json(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    """Same as /login but accepts JSON instead of form-encoded data —
    convenient for the React frontend."""
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.id, "role": user.role.value})
    return schemas.TokenResponse(access_token=access_token, user=schemas.UserOut.model_validate(user))
