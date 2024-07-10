from pydantic import BaseModel, EmailStr
from typing import Optional, Any


class SignUp(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool = True
    is_staff: bool = False


class LoginModel(BaseModel):
    username_or_email: str
    password: str


class Settings(BaseModel):
    authjwt_secrets_key: str = '9f2b6edbe6a456f18b1328deaeae9d8ef2ac5bcb606fffc5dd7d92d287d9e66a'
