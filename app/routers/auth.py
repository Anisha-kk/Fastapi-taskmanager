# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from app.core.security import create_access_token,get_password_hash,verify_password
from app.models import user as user_model
from app.schemas import user as user_schema
from app.db.session import get_db
from logger.logger import Logger

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

info_logger = Logger.logger("infoLogger")

# Signup route
@router.post("/signup", response_model=user_schema.UserOut)
def signup(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    info_logger.info("Signing up new user")
    existing_user = db.query(user_model.User).filter(user_model.User.email == user.email).first()
    if existing_user:
        info_logger.error("User is already registered")
        raise HTTPException(status_code=400, detail="User already registered")
    hashed_password = get_password_hash(user.password)
    new_user = user_model.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    info_logger.info("User signed up")
    return new_user

# Login route
@router.post("/login")
def login(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    info_logger.info("Logging in...")
    db_user = db.query(user_model.User).filter(user_model.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        info_logger.error("Invalid login credentials")
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": str(db_user.username)})
    return {"access_token": access_token, "token_type": "bearer"}
