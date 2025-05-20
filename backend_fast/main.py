from typing import Union

from fastapi import FastAPI
from db.database import Base, engine
from routes import users, orders, order_items, items, auth

app = FastAPI()
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(order_items.router)
app.include_router(items.router)
app.include_router(auth.router)


@app.on_event("startup")
def startup_event():
    # Perform any startup tasks here
    Base.metadata.create_all(bind=engine)
    # For example, you can create the database tables


# @app.get("/health")
# def health_check():
#     try:
#         conn()
#         return {"status": "healthy"}
#     except Exception as e:
#         return {"status": "unhealthy", "error": str(e)}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
