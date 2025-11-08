from pydantic import BaseModel, EmailStr, field_validator

class User(BaseModel):
    name: str
    email: EmailStr
    account_id: int

    @field_validator("account_id")
    def validate_account_id(cls, value):
        if value < 0:
            raise ValueError(f"account_id must be positive: {value}")
        return value

user = User(
    name="Tomas",
    email="tomas@gmail.com",
    account_id=1
)

print(user.model_dump_json())