from pydantic import BaseModel, EmailStr


class TokenScheme(BaseModel):
    access_token: str
    token_type: str


class TokenDataScheme(BaseModel):
    id: int


class AuthScheme(BaseModel):
    username: str
    password: str


class SignUpScheme(AuthScheme):
    email: EmailStr | None = None
