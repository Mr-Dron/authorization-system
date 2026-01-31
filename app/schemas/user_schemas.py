from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

from app.validatos.schemas_validators.value_validators import PasswordValidatorMixin, ValueValidatorMixin, CorrectPasswordValidatorMixin

class UserRegistration(PasswordValidatorMixin, ValueValidatorMixin, CorrectPasswordValidatorMixin, BaseModel):

    first_name: str
    last_name: str
    email: EmailStr
    description: Optional[str]=None
    password: str
    repeated_password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    description: Optional[str] = None


class UserOut(BaseModel):

    first_name: str
    last_name: str
    email: str
    description: str

    model_config = ConfigDict(from_attributes=True)