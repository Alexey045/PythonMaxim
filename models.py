from pydantic import BaseModel
from typing import Optional, List


class ObjectData(BaseModel):
    objectID: int
    title: str
    artistDisplayName: str
    objectDate: str
    medium: str
    department: str
    isHighlight: bool
    objectURL: str


class Objects(BaseModel):
    total: int
    objectIDs: List[int]


class SearchResult(BaseModel):
    total: int
    objectIDs: List[int]


class Department(BaseModel):
    departmentId: int
    displayName: str


class Departments(BaseModel):
    departments: List[Department]
