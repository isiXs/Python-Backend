from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str

products_list = [Product(id=1, name="Laptop", price=1000.0, description="Laptop description"),
                    Product(id=2, name="Mouse", price=20.0, description="Mouse description"),
                    Product(id=3, name="Keyboard", price=50.0, description="Keyboard description")]


@router.get("/products")
async def products():
    return products_list;

@router.get("/products({id})")
async def products(id: int):
    return search_products(id);


def search_products(id: int):
    products_filter = filter(lambda product: product.id == id, products_list)
    return next(products_filter,{"error": "product not found"} )