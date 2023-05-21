from jose import jwt, JWTError
from typing import TypedDict
from datetime import datetime, timedelta
from fastapi import Response, Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from passlib.context import CryptContext
import src.exceptions as exc

SECRET_KEY = "3898b1713cd001b4e6b41be328ab344b697baff8b100da072ae6c62fdedd6f45"
REFRESH_SECRET_KEY = "3c8bd764b516841308d9db68ae8c48b61a7d351daf6e5c49c7a9e31ec0c4c508"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: str | None = None,
        scopes: dict[str, str] | None = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})  # type: ignore
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> str | None:
        authorization = request.cookies.get("access_token")

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise exc.NotAuthenticated()
            else:
                return None
        return param


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="auth/token", scheme_name="JWT")


def get_password_hash(password: str) -> str:
    hash_pass: str = pwd_context.hash(password)
    return hash_pass


def verify_password(plain_password: str, hashed_password: str) -> bool:
    verify: bool = pwd_context.verify(plain_password, hashed_password)
    return verify


def create_access_token(
    data: dict[str, str | datetime], expires_delta: timedelta | None = None
) -> str:
    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    data.update({"exp": expire})
    encoded_jwt: str = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    data: dict[str, str | datetime], expires_delta: timedelta | None = None
) -> str:
    expire = datetime.utcnow() + (
        expires_delta
        if expires_delta
        else timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    )
    data.update({"exp": expire})
    encoded_jwt: str = jwt.encode(data, REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


async def require_refresh_token(request: Request) -> str | None:
    authorization = request.cookies.get("refresh_token")

    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        raise exc.NotAuthenticated()
    return param


def set_cookie(
    response: Response, access_token: str, refresh_token: str, logged_in: bool = False
) -> None:
    if access_token:
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
        )
    if refresh_token:
        response.set_cookie(
            key="refresh_token",
            value=f"Bearer {refresh_token}",
            max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
            expires=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
        )
    if logged_in:
        response.set_cookie(
            key="logged_in",
            value="True",
            max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
            expires=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        )


class PayloadType(TypedDict):
    sub: str
    exp: float


def decode_token(token: str) -> str:
    try:
        payload: PayloadType = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if (username := payload.get("sub")) is None:
            raise exc.ValidateCredentials()
    except JWTError:
        raise exc.ValidateCredentials()
    assert (exp := payload.get("exp"))
    if datetime.fromtimestamp(exp) < datetime.now():
        raise exc.TokenExpired()
    return username


def decode_refresh_token(token: str) -> str:
    try:
        payload: PayloadType = jwt.decode(
            token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM]
        )
        if (username := payload.get("sub")) is None:
            raise exc.ValidateCredentials()
    except JWTError:
        raise exc.ValidateCredentials()
    assert (exp := payload.get("exp"))
    if datetime.fromtimestamp(exp) < datetime.now():
        raise exc.TokenExpired(detail="Refresh token expired")
    return username
