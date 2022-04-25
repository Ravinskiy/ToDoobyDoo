
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
from typing import List, Dict, Optional
from fastapi import FastAPI, Query, Response, status
from pydantic import BaseModel
app = FastAPI()
db_conn = sqlite3.connect('data/todoobydo.sqlite')
# db_conn.row_factory = sqlite3.Row  # Make sqlite output records with headers
cursor = db_conn.cursor()
db_conn.execute(
    "CREATE TABLE if not exists items \
    (id integer primary key, description text, done text)"
)
db_conn.commit()
db_conn.close()


class Item(BaseModel):
    description: str
    done: str = 'No'
    id: Optional[int] = 0


class ItemIn(BaseModel):
    description: str


@app.post("/items/", status_code=status.HTTP_201_CREATED)
def post_item(item: ItemIn) -> int:
    item.done = 'No'
    db_conn = sqlite3.connect('data/todoobydo.sqlite')
    db_conn.row_factory = sqlite3.Row
    cursor = db_conn.cursor()
    query = "INSERT INTO items(description, done) VALUES (?, ?)"
    cursor.execute(query, (item.description, item.done))
    db_conn.commit()
    db_conn.close()
    return item


@app.get("/items/all", status_code=status.HTTP_200_OK)
def get_all_items(response: Response) -> List[dict]:
    db_conn = sqlite3.connect('data/todoobydo.sqlite')
    db_conn.row_factory = sqlite3.Row
    cursor = db_conn.cursor()
    query = "SELECT id, description, done FROM items"
    rows = cursor.execute(query).fetchall()
    output = []
    if rows:
        for row in rows:
            record = dict(row)
            output.append(record)
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
    db_conn.close()
    return output


@app.get("/items/{item_id}", status_code=status.HTTP_200_OK)
def get_item(item_id: int, response: Response) -> dict:
    db_conn = sqlite3.connect('data/todoobydo.sqlite')
    db_conn.row_factory = sqlite3.Row
    cursor = db_conn.cursor()
    query = "SELECT id, description, done FROM items WHERE id=?"
    row = cursor.execute(query, (item_id, )).fetchone()
    if row:
        output = dict(row)
    else:
        output = {}
        response.status_code = status.HTTP_404_NOT_FOUND
    db_conn.close()
    return output


@app.get("/items/{item_id}/status", status_code=status.HTTP_200_OK)
async def get_item_status(item_id: int, response: Response) -> dict:
    db_conn = sqlite3.connect('data/todoobydo.sqlite')
    db_conn.row_factory = sqlite3.Row
    cursor = db_conn.cursor()
    query = "SELECT id, description, done FROM items WHERE id=?"
    row = cursor.execute(query, (item_id, )).fetchone()
    if row:
        record = dict(row)
        output = {
            'done': record['done']
        }
    else:
        output = {}
        response.status_code = status.HTTP_404_NOT_FOUND
    db_conn.close()
    return output


@app.put("/items/{item_id}/status", status_code=status.HTTP_200_OK)
def update_item_status(
    item_id: int,
    response: Response,
    done: str = Query('No', regex=r"(Yes|No)")
) -> dict:
    db_conn = sqlite3.connect('data/todoobydo.sqlite')
    db_conn.row_factory = sqlite3.Row
    cursor = db_conn.cursor()
    query = "SELECT id, description, done FROM items WHERE id=?"
    row = cursor.execute(query, (item_id, )).fetchone()
    if row:
        query_upd = "UPDATE items SET done=? WHERE id=?"
        cursor.execute(query_upd, (done, item_id))
        db_conn.commit()
    else:
        output = {}
        response.status_code = status.HTTP_404_NOT_FOUND
    output = {
        'id': item_id,
        'done': done
    }
    db_conn.close()
    return output


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> Dict[str, int]:
    db_conn = sqlite3.connect('data/todoobydo.sqlite')
    db_conn.row_factory = sqlite3.Row
    cursor = db_conn.cursor()
    query_del = "DELETE FROM items WHERE id=?"
    cursor.execute(query_del, (item_id, ))
    db_conn.commit()
    output = {
        'id': item_id
    }
    db_conn.close()
    return output
