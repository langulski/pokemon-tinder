import datetime as dt
from typing import Dict, List
from fastapi import Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from pydantic import BaseModel

from src.models.user import User
from src.database.database import pgcursor
from src.schemas.settings import settings
from src.schemas.auth_cookie import OAuth2PasswordBearerWithCookie




def get_user(email: str) -> User:
    conn,cursor = pgcursor()
    query = "SELECT id,name,email,password,active FROM USERS WHERE email='{}';".format(email)
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    user = [
        {column_name: value for column_name, value in zip(column_names, row)}
        for row in rows
    ]
    cursor.close()
    conn.close()
    if user:
        if user[0].get("active"):
            return user[0]
    return None


templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token")


def create_access_token(data: Dict) -> str:
    to_encode = data.copy()
    expire = dt.datetime.utcnow() + dt.timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def authenticate_user(email: str, plain_password: str) -> User:
    user = get_user(email)
    if not user:
        return False
    if not crypto.verify(plain_password, user.get("password")):
        return False
    del user['password']
    return user


def decode_token(token: str) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
    )
    if token:
        token = token.removeprefix("Bearer").strip()
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError as e:
        print(e)
        raise credentials_exception

    user = get_user(email)
    del user["password"]
    return user


def get_current_user_from_token(token: str = Depends(oauth2_scheme)) -> User:
    """
    Get the current user from the cookies in a request.

    Use this function when you want to lock down a route so that only
    authenticated users can see access the route.
    """
    user = decode_token(token)
    return user


def get_current_user_from_cookie(request: Request) -> User:
    """
    Get the current user from the cookies in a request.

    Use this function from inside other routes to get the current user. Good
    for views that should work for both logged in, and not logged in users.
    """
    try:
        token = request.cookies.get(settings.COOKIE_NAME)
        user = decode_token(token)
        return user
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
        )
