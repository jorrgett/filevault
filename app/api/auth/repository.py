from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Sequence
from sqlalchemy.future import select

from app.helpers.mails.forget_password import forgetPasswordMail
from app.api.auth.schemas import UserLoginSchema
from app.helpers.jwt_handler import decodeJWT, signJWT
from app.api.applications.models import Application
from app.resources import strings


from app.helpers.jwt_handler import (
    verify_password, signJWT
)


class AuthRepository():
    def __init__(self, session: Session):
        self.session = session

    def login(
        self,
        payload,
        user,
    ):

        get_user = user.get_by_email(email=payload.email)

        if not get_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": 2,
                    "message": strings.USER_DOES_NOT_AUTHENTICABLE
                }
            )

        verify_password(
            payload.password,
            get_user.password
        )

        return self.response_with_token(get_user)

    def forget_password(
        self,
        payload,
        user
    ):
        get_user = user.get_by_email(email=payload.email)

        if not get_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "message": strings.USER_DOES_NOT_FOUND_EMAIL
                }
            )

        generate_code = user.set_token_to_recovery(
            user_id=get_user.id
        )

        if generate_code.code:
            return forgetPasswordMail().send(
                subject='Recuperar contraseña',
                to=get_user.email,
                name=get_user.full_name,
                code=generate_code.code
            )

        return generate_code

    def get_last_sequence(self, sequence):
        seq = Sequence(sequence)
        result = self.session.execute(seq)

        return result

    def response_with_token(self, user):

        jwt = signJWT(email=user.email, service=False, in_minutes=60)
        refresh = signJWT(email=user.email, service=False, in_minutes=1440)

        return {
            'authorization': {
                'access_token': jwt,
                'refresh_token': refresh,
                'ttl': 3600
            },
            'user': user,
        }

    def reset_password(
        self,
        payload,
        user
    ):
        get_user = user.check_user_request_recovery(
            code=payload.code
        )

        if not get_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": f"The code has expired, request a new one: {payload.code}"},
            )

        new_password = payload.password

        user.update(
            user_id=get_user.id,
            payload=payload
        )

        return self.login(
            payload=UserLoginSchema(
                email=get_user.email,
                password=new_password
            ),
            user=user
        )

    def refresh(
        self,
        payload,
        user
    ):
        decode = decodeJWT(payload.token, False)

        if not decode:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "message": "The refresh token is expired, please login again"
                })

        result = user.get_by_email(email=decode['email'])
        return self.response_with_token(result)

    def generate_token(self, payload):

        query = self.session.execute(
            select(Application).where(
                (Application.code == payload.code)
            )
        )
        app = query.scalars().first()

        if app is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "message": f"No app with this code: {payload.code} has been found"},
            )

        if app.secret != payload.secret_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "message": f"The secret key entered is not valid"},
            )

        jwt = signJWT(service=True, app_id=app.id, in_minutes=20160)
    
        return {
            'token': jwt
        }
