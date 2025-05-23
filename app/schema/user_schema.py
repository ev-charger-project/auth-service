import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from app.schema.base_schema import ModelBaseInfo, PaginationQuery
from app.util.schema import AllOptional


class _BaseUser(BaseModel):
    email: str
    name: str = Field(max_length=50)
    is_active: bool = True
    phone_number: Optional[str]

    class Config:
        orm_mode = True


class UserResponse(ModelBaseInfo, _BaseUser, metaclass=AllOptional):
    image_url: Optional[str] = None
    password: str
    is_superuser: bool = False


class CreateUser(_BaseUser, metaclass=AllOptional):
    password: str
    is_superuser: bool = False

    @field_validator("email")
    def email_validator(cls, value):
        if not value:
            raise ValueError("email is required")
        regex = re.compile(
            r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])"
        )
        if not regex.match(value):
            raise ValueError("email is invalid")
        return value

    @field_validator("phone_number")
    def phone_number_validator(cls, value):
        if value:
            regex = re.compile(r"^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$")
            if not regex.match(value):
                raise ValueError("phone number is invalid")
        return value


class UpdateUser(_BaseUser, metaclass=AllOptional):
    is_superuser: bool = False
    image_url: Optional[str] = None


class FindUser(PaginationQuery, _BaseUser, metaclass=AllOptional):
    pass
