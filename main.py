
'''
API for ToDo list
design and write a CRUD service in python or node.js for a to-do list
that will support reading list, adding new items, marking items as done,
delete items.

Remarks -
The list should be available even if the service is restarted.
Add tests
share your code in git
include a clear README file that will describe how to build and use the API
'''
import sqlite3
from typing import List, Dict
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
app = FastAPI()
db_conn = sqlite3.connect('data/todoobydo.db')


class Item(BaseModel):
    text: str


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def post_item(item: Item, response: Response) -> int:
    output = item_id
    return output


@app.get("/items/all", status_code=status.HTTP_200_OK)
async def get_all_items(response: Response) -> List[dict]:
    output = []
    return output


@app.get("/items/{item_id}", status_code=status.HTTP_200_OK)
async def get_item(item_id: int, response: Response) -> dict:
    output = {
        'id': item_id,
        'done': done,
        'text': item_text
    }
    return output


@app.get("/items/{item_id}/status", status_code=status.HTTP_200_OK)
async def get_item_status(item_id: int, response: Response) -> dict:
    output = {
        'id': item_id,
        'done': done
    }
    return output


@app.put("/items/{item_id}/status", status_code=status.HTTP_200_OK)
async def update_item_status(
    item_id: int,
    response: Response,
    done: bool = False
) -> dict:
    output = {
        'id': item_id,
        'done': done
    }
    return output


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, response: Response) -> Dict[str, int]:
    output = {
        'id': item_id
    }
    return output
