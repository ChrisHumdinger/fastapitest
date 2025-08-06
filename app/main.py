from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine, async_session
from app.models import Item
from app.schemas import ItemCreate, ItemUpdate, ItemOut


app = FastAPI(title="Coolify FastAPI Postgres Demo")

app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],)

# Create tables at startup
@app.on_event("startup")
async def on_startup():
   async with engine.begin() as conn:
       await conn.run_sync(Base.metadata.create_all)

# Dependency for DB session
async def get_db():
   async with async_session() as session:
       yield session

@app.post("/items", response_model=ItemOut)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
   db_item = Item(name=item.name, description=item.description)
   db.add(db_item)
   await db.commit()
   await db.refresh(db_item)
   return db_item

@app.get("/items", response_model=list[ItemOut])
async def list_items(db: AsyncSession = Depends(get_db)):
   result = await db.execute(select(Item))
   items = result.scalars().all()
   return items

@app.get("/items/{item_id}", response_model=ItemOut)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
   result = await db.execute(select(Item).where(Item.id == item_id))
   item = result.scalar_one_or_none()
   if not item:
       raise HTTPException(status_code=404, detail="Item not found")
   return item

@app.patch("/items/{item_id}", response_model=ItemOut)
async def update_item(item_id: int, item: ItemUpdate, db: AsyncSession = Depends(get_db)):
   result = await db.execute(select(Item).where(Item.id == item_id))
   db_item = result.scalar_one_or_none()
   if not db_item:
       raise HTTPException(status_code=404, detail="Item not found")
   for field, value in item.dict(exclude_unset=True).items():
       setattr(db_item, field, value)
   db.add(db_item)
   await db.commit()
   await db.refresh(db_item)
   return db_item

@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
   result = await db.execute(select(Item).where(Item.id == item_id))
   db_item = result.scalar_one_or_none()
   if not db_item:
       raise HTTPException(status_code=404, detail="Item not found")
   await db.delete(db_item)
   await db.commit()
   return None


