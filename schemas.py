from pydantic import BaseModel, Field


# Esquema para validar la creacion de productos de los datos que llegan desde el front
class CreateProduct(BaseModel):
    sku: str = Field(min_length=3, max_length=3)
    name: str = Field(min_length=3, max_length=75)
    price: float


class UpdateProduct(BaseModel):
    name: str = Field(min_length=3, max_length=75)
    price: float
