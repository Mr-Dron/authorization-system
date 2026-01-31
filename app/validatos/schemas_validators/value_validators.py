from pydantic import field_validator, model_validator

import re 

class PasswordValidatorMixin:

    @field_validator("password", mode="before")
    def validate_password(cls, value: str):

        if len(value) < 8:
            raise ValueError("The password length must be greater than 8")
        if not re.search(r"[a-z]", value):
            raise ValueError("The password must contain a lowercase letter")
        if not re.search(r"[A-Z]", value):
            raise ValueError("The password must contain a capital letter")
        if not re.search(r"[0-9]", value):
            raise ValueError("The password must contain a number")
        
        return value

class ValueValidatorMixin:

    veriables = ["first_name", "last_name"]

    @model_validator(mode="after")
    def velidate_value(self):

        for veriable in self.veriables:
            try:
                value = getattr(self, veriable)

                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f"Field {veriable} cannot be empty")
            
            except Exception:
                continue
        
        return self 


class CorrectPasswordValidatorMixin:

    @model_validator(mode="after")
    def validate_pass(self):
        
        if self.password != self.repeated_password:
            raise ValueError("Passwords must be odinakovie))") #TODO нормальный перевод

        return self