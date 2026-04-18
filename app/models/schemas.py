
from pydantic import AliasChoices, BaseModel, ConfigDict, EmailStr, Field


# Auth schemas
class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ProfileUpdateRequest(BaseModel):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class VerifyOTPRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    email: EmailStr
    otp_code: str = Field(
        ...,
        min_length=6,
        max_length=6,
        validation_alias=AliasChoices("otp_code", "otp"),
    )


class ResetPasswordRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    reset_token: str = Field(
        ...,
        validation_alias=AliasChoices("reset_token", "token"),
    )
    new_password: str = Field(..., min_length=6)


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6)


# Portfolio schemas
class PortfolioRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    portfolio_type: str = "Equity"


class HoldingRequest(BaseModel):
    stock_symbol: str = Field(..., min_length=1, max_length=10)
    stock_name: str = Field(..., min_length=1)
    quantity: float = Field(..., gt=0)
    buy_price: float = Field(..., gt=0)
    sector: str | None = None


class PriceUpdateRequest(BaseModel):
    new_price: float = Field(..., gt=0)


# Market analysis schemas
class AnalyzeRequest(BaseModel):
    stock_symbol: str = Field(..., min_length=1, max_length=10)
    stock_name: str | None = None
    current_price: float | None = None
    sector: str | None = None
