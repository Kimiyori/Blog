from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from passlib.context import CryptContext

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
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearerWithCookie(
    tokenUrl="users/token", scheme_name="JWT"
)


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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return param
