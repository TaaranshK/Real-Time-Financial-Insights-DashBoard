from pydantic import BaseModel


class AlertCreate(BaseModel):
    asset_name: str
    target_price: float
    condition: str   


class AlertResponse(BaseModel):
    id: int
    asset_name: str
    target_price: float
    condition: str

    class Config:
        from_attributes = True
