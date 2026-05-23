new_router = open("inventory-service/app/routers/inventory_router.py", "r", encoding="utf-8").read()

stock_endpoints = """
from pydantic import BaseModel as PydanticBaseModel

class StockAdjustRequest(PydanticBaseModel):
    quantity: int

@router.get("/books/{book_id}")
def get_book_stock(book_id: str, db: Session = Depends(get_db)):
    from app.infrastructure.models import InventoryItemModel
    item = db.query(InventoryItemModel).filter(
        InventoryItemModel.book_reference == book_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Libro no encontrado en inventario")
    return {
        "book_id": book_id,
        "quantity": item.quantity_available,
        "condition": item.condition,
        "quantity_reserved": item.quantity_reserved,
    }

@router.post("/books/{book_id}/deduct")
def deduct_stock(book_id: str, request: StockAdjustRequest, db: Session = Depends(get_db)):
    from app.infrastructure.models import InventoryItemModel
    item = db.query(InventoryItemModel).filter(
        InventoryItemModel.book_reference == book_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Libro no encontrado en inventario")
    if item.quantity_available < request.quantity:
        raise HTTPException(status_code=409, detail="Stock insuficiente")
    item.quantity_available -= request.quantity
    db.commit()
    return {"book_id": book_id, "quantity_available": item.quantity_available}

@router.post("/books/{book_id}/restore")
def restore_stock(book_id: str, request: StockAdjustRequest, db: Session = Depends(get_db)):
    from app.infrastructure.models import InventoryItemModel
    item = db.query(InventoryItemModel).filter(
        InventoryItemModel.book_reference == book_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Libro no encontrado en inventario")
    item.quantity_available += request.quantity
    db.commit()
    return {"book_id": book_id, "quantity_available": item.quantity_available}
"""

with open("inventory-service/app/routers/inventory_router.py", "w", encoding="utf-8") as f:
    f.write(new_router + stock_endpoints)
print("Done")
