from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class ProductRequest(BaseModel):
    name: str = Field(
        None, title="Product Name", max_length=1000
    )
    price: float = Field(..., gt=0,
                         description="Price of the product")
    is_available: bool = Field(
        False, description="Value must be either True or False")
    seller_email: EmailStr = Field(None, title="Seller Email")
    created_by: int = Field(None, title="User Id")


class ProductUpdateRequest(BaseModel):
    product_id: int
    name: str = Field(
        None, title="Product Name", max_length=1000
    )
    price: float = Field(..., gt=0,
                         description="The price must be greater than zero")
    is_available: bool = Field(
        False, description="Value must be either True or False")
    seller_email: Optional[EmailStr] = Field(None, title="Updater Email")
    updated_by: int = Field(None, title="Updater Id")