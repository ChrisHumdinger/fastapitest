from pydantic import BaseModel, Field
from typing import Optional

class ItemBase(BaseModel):
   name: str = Field(..., max_length=100)
   description: Optional[str] = None

class ItemCreate(ItemBase):
   pass

class ItemUpdate(BaseModel):
   name: Optional[str] = Field(None, max_length=100)
   description: Optional[str] = None

class ItemOut(ItemBase):
   id: int

   class Config:
       orm_mode = True
