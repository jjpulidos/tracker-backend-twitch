from typing import Optional
import pymongo
import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import json
app = FastAPI()

class Post(BaseModel):
    id: str
    content: str
    url: str
    category: str


def conn():
    client = pymongo.MongoClient(
        "mongodb+srv://dbUser:Q1w2e3r4t5@cluster0.gpcjm.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client["tracker-reels"]
    posts = db['posts']
    return posts

posts = conn()


@app.get("/")
def read_post():
    post = posts.find_one()
    post["_id"] = str(post.get("_id"))
    return {"post": post}


@app.post("/create_post")
def create_post(post: Post):
    try:
        post_json = {
            "_id": post.id,
            "content": post.content,
            "url": post.url,
            "category": post.category
        }
        id = posts.insert_one(post_json)
    except Exception as ex:
        print(ex)
        return "Error with Insertion"
    return f"Inserted post with ID: {id}"




@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}







