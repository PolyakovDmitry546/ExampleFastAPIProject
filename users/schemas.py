from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr | None = None
    password: str


class UserOut(BaseModel):
    id: int | None = None
    username: str
    email: EmailStr | None = None


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
