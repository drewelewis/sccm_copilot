import json
from typing import List
from pydantic import BaseModel,Json,create_model
from marshmallow import Schema, fields


class SCCMQuery(BaseModel):
    query: str

class Table(BaseModel, extra='allow'):
    name: str

class QueryResponse():
    def __init__(self, comments: str, method: str, url: str,query: json, final_comments: str):
        self.comments = comments
        self.method = method
        self.url = url
        self.query = query
        self.final_comments = final_comments


    
