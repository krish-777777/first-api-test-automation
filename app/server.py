from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, conlist
from typing import Dict, Optional, List, Annotated
import logging
from framework.logger import get_app_logger

app = FastAPI(title="Demo CRUD API")
logger = get_app_logger()

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    description: Optional[str] = Field(None, max_length=500)
    tags: Optional[Annotated[List[str], Field(max_length=10)]] = None

DB: Dict[int, Item] = {}
NEXT_ID = 1

@app.post("/items")
def create_item(item: Item):
    global NEXT_ID
    item_id = NEXT_ID
    NEXT_ID += 1
    DB[item_id] = item
    logger.info(f"Created item {item_id}: {item.model_dump()}")
    return {"id": item_id, **item.model_dump()}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = DB.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **item.model_dump()}

@app.get("/items")
def list_items():
    return [{"id": i, **item.model_dump()} for i, item in DB.items()]

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Item not found")
    DB[item_id] = item
    logger.info(f"Updated item {item_id}: {item.model_dump()}")
    return {"id": item_id, **item.model_dump()}

@app.patch("/items/{item_id}")
def patch_item(item_id: int, item: Item):
    # FastAPI will already validate fields; simulate partial by merging with existing
    existing = DB.get(item_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Item not found")
    data = existing.model_dump()
    for k, v in item.model_dump(exclude_unset=True).items():
        data[k] = v
    patched = Item(**data)
    DB[item_id] = patched
    logger.info(f"Patched item {item_id}: {patched.model_dump()}")
    return {"id": item_id, **patched.model_dump()}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Item not found")
    del DB[item_id]
    logger.info(f"Deleted item {item_id}")
    return {"deleted": item_id}
