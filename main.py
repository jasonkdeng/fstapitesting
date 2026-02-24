from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    text: str = None
    is_done: bool = False

@app.get("/")
def root():
    return {"message": "Hello, World!"}

items = []
@app.post("/items")
# Item class has to be queried as a json object, which contains more information
# Query as {"text": "apple", "is_done"=false} from text: str, is_done: bool
def create_item (item: Item):
    items.append(item)
    return items

@app.get ("/items", response_model=list[Item])
def list_items (limit: int = 10) -> str:
    if limit <= len(items):
        return items[0, limit]
    else:
        raise HTTPException(status_code=404, detail=f"There are only {len(items)} items")

@app.get("/items/{item_id}", response_model=Item)
def get_item (item_id: int) -> str: 
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    else:
        item = items[item_id]
        return item