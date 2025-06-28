from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field 
from typing import Optional, List
import json

app = FastAPI(title='FastInventory', description='API para gestión de productos y categorías', version='1.0.0')

# ========== Schemas ==========
class CategoryBase(BaseModel):
    id: int = Field(..., gt=0, )
    name: str = Field(..., min_length=3, max_length=50, )

class ProductBase(BaseModel):
    sku: str = Field(..., min_length=3, max_length=10, )
    name: str = Field(..., min_length=3, max_length=75, )
    price: float = Field(..., gt=0, description="Precio debe ser mayor a 0", )
    category_id: int = Field(..., description="ID de categoría existente",)

   

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=75)
    price: Optional[float] = Field(None, gt=0)
    category_id: Optional[int] = Field(None, gt=0)

    

# ========== Helper Functions ==========
def read_db():
    with open('db.json', 'r') as db:
        return json.load(db)

def write_db(data):
    with open('db.json', 'w') as db:
        json.dump(data, db, indent=2)

def category_exists(category_id: int) -> bool:
    data = read_db()
    return any(cat['id'] == category_id for cat in data['categories'])

def is_category_in_use(category_id: int) -> bool:
    data = read_db()
    return any(product['category_id'] == category_id for product in data['products'])

# ========== Category Endpoints ==========
@app.get('/categories', response_model=List[CategoryBase], tags=["Categorías"])
def get_categories():
    """Obtiene todas las categorías disponibles"""
    return read_db()['categories']

@app.post('/categories', status_code=status.HTTP_201_CREATED, tags=["Categorías"])
def create_category(category: CategoryBase):
    """Crea una nueva categoría"""
    data = read_db()
    
    if any(cat['id'] == category.id for cat in data['categories']):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La categoría con ID {category.id} ya existe"
        )
    
    data['categories'].append(category.dict())
    write_db(data)
    return {"message": "Categoría creada exitosamente", "category": category}

@app.put('/categories/{category_id}', tags=["Categorías"])
def update_category(category_id: int, category: CategoryBase):
    """Actualiza una categoría existente"""
    data = read_db()
    
    for index, cat in enumerate(data['categories']):
        if cat['id'] == category_id:
            # Verificar si el nuevo ID ya existe (si es diferente al actual)
            if category.id != category_id and any(c['id'] == category.id for c in data['categories']):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El ID {category.id} ya está en uso por otra categoría"
                )
            
            data['categories'][index] = category.dict()
            write_db(data)
            return {"message": "Categoría actualizada exitosamente", "category": category}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Categoría con ID {category_id} no encontrada"
    )

@app.delete('/categories/{category_id}', tags=["Categorías"])
def delete_category(category_id: int):
    """Elimina una categoría si no está en uso por productos"""
    data = read_db()
    
    if is_category_in_use(category_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar la categoría porque está asociada a productos existentes"
        )
    
    for index, cat in enumerate(data['categories']):
        if cat['id'] == category_id:
            data['categories'].pop(index)
            write_db(data)
            return {"message": f"Categoría con ID {category_id} eliminada exitosamente"}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Categoría con ID {category_id} no encontrada"
    )

# ========== Product Endpoints ==========
@app.get('/products', tags=["Productos"])
def get_products():
    """Obtiene todos los productos con información de categoría"""
    data = read_db()
    result = []
    
    for product in data['products']:
        category = next((cat for cat in data['categories'] if cat['id'] == product['category_id']), None)
        product_with_category = {
            **product,
            "category_name": category['name'] if category else "Sin categoría"
        }
        result.append(product_with_category)
    
    return result

@app.post('/products', status_code=status.HTTP_201_CREATED, tags=["Productos"])
def create_product(product: ProductBase):
    """Crea un nuevo producto validando la categoría"""
    if not category_exists(product.category_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La categoría con ID {product.category_id} no existe"
        )
    
    data = read_db()
    
    if any(p['sku'] == product.sku for p in data['products']):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El SKU {product.sku} ya está registrado"
        )
    
    data['products'].append(product.dict())
    write_db(data)
    return {"message": "Producto creado exitosamente", "product": product}

@app.put('/products/{sku}', tags=["Productos"])
def update_product(sku: str, product: ProductUpdate):
    """Actualiza un producto existente"""
    data = read_db()
    
    for index, p in enumerate(data['products']):
        if p['sku'] == sku.upper():
            update_data = product.dict(exclude_unset=True)
            
            # Validar categoría si se está actualizando
            if 'category_id' in update_data and not category_exists(update_data['category_id']):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"La categoría con ID {update_data['category_id']} no existe"
                )
            
            updated_product = {**p, **update_data}
            data['products'][index] = updated_product
            write_db(data)
            return {"message": "Producto actualizado exitosamente", "product": updated_product}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Producto con SKU {sku} no encontrado"
    )

@app.delete('/products/{sku}', tags=["Productos"])
def delete_product(sku: str):
    """Elimina un producto existente"""
    data = read_db()
    
    for index, p in enumerate(data['products']):
        if p['sku'] == sku.upper():
            data['products'].pop(index)
            write_db(data)
            return {"message": f"Producto con SKU {sku} eliminado exitosamente"}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Producto con SKU {sku} no encontrado"
    )

# ========== Documentation ==========
@app.get('/', response_class=HTMLResponse, include_in_schema=False)
def home_page():
    return """
    <h1>FastInventory API</h1>
    <p>Documentación interactiva disponible en <a href='/docs'>/docs</a></p>
    """