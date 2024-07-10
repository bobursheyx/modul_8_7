import datetime
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import or_
from database import SessionLocal
from schemas import SignUp, LoginModel
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

auth_router = APIRouter(prefix="/auth")


# Configure AuthJWT
@AuthJWT.load_config
def get_config():
    return {
        'SECRET_KEY': 'your-secret-key',
        'ALGORITHM': 'HS256',
        'ACCESS_TOKEN_EXPIRE_MINUTES': 60,
        'REFRESH_TOKEN_EXPIRE_DAYS': 3,
        'TOKEN_BLACKLIST_ENABLED': True,
        'TOKEN_BLACKLIST_STORE': set(),
    }


@auth_router.post('/logout', status_code=status.HTTP_200_OK)
async def logout(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        jti = Authorize.get_raw_jwt()['jti']
        Authorize.token_in_blacklist(jti)
        return {"message": "Successfully logged out"}
    except AuthJWTException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: SignUp):
    session = SessionLocal()
    db_user = session.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    db_user = session.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    hashed_password = generate_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, password=hashed_password,
                    is_active=user.is_active, is_staff=user.is_staff)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "User created successfully", "new_user": new_user}


@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    session = SessionLocal()
    db_user = session.query(User).filter(
        or_(
            User.username == user.username_or_email,
            User.email == user.username_or_email
        )
    ).first()
    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)
        return {
            "message": "Successfully logged in",
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
