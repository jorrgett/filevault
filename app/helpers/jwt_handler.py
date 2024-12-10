from fastapi import HTTPException, status

from datetime import datetime, timedelta
from typing import Dict

import jwt
from decouple import config
from passlib.context import CryptContext
from app.resources.strings import (
    USER_DOES_NOT_AUTHENTICABLE
)

JWT_SECRET = config("SECRET_KEY")
JWT_ALGORITHM = config("JWT_ALGORITHM")
JWT_SERVICE_S3 = config("SECRET_KEY_SERVICE")


def signJWT(**args) -> Dict[str, str]:

    now = datetime.now()
    time_base = timedelta(minutes=args['in_minutes'])
    expire = now + time_base

    payload = {
        "expires": expire.strftime("%m/%d/%Y, %H:%M:%S")
    }

    if args['service']:
        payload['app_id'] = args['app_id']
        secret = JWT_SERVICE_S3

    else:
        payload['email'] = args['email']
        secret = JWT_SECRET

    return jwt.encode(payload, secret, algorithm=JWT_ALGORITHM)


def decodeJWT(token: str, service: bool = False) -> dict:
    time_now = (datetime.now()).strftime("%m/%d/%Y, %H:%M:%S")

    if service:
        secret = JWT_SERVICE_S3
    else:
        secret = JWT_SECRET

    try:
        decoded_token = jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])

        return decoded_token if decoded_token["expires"] >= time_now else None
    except:
        return {}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    check = pwd_context.verify(plain_password, hashed_password)

    if not check:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": 2,
                "message": USER_DOES_NOT_AUTHENTICABLE
            }
        )

    return check


def get_password_hash(password):
    return pwd_context.hash(password)
