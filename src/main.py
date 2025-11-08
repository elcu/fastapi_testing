from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    text: str = None
    is_done: bool = False



@app.get("/")
def root():
    return {"hello": "world"}

items = []
@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items

@app.get("/items", response_model=list[Item])
def list_items(limit: int = 5):
    return items[0:limit]

@app.get("/items/{item_number}", response_model=Item)
def get_item(item_number: int) -> Item:
    if item_number < len(items):
        return items[item_number]
    else:
        raise HTTPException(status_code=404, detail = "Item was not found.")


# curl -X POST -H "Content-Type: application/json" 'http://127.0.0.1:8000/items?item=apple'
# curl -H "Content-Type: application/json" 'http://127.0.0.1:8000/items/0'
# curl -H "Content-Type: application/json" 'http://127.0.0.1:8000/items?limit=8'

# with BaseModel
# no longer the data are in query at the end of url, they are instead json payload sent via -d (data)
# curl -X POST -H "Content-Type: application/json" -d '{"text": "apple"}' 'http://127.0.0.1:8000/items'