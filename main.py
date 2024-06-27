from fastapi import FastAPI, WebSocket, HTTPException, Depends
from pydantic import BaseModel
import datetime
import random
import asyncio
from typing import Dict

app = FastAPI()

# In-memory database
orders_db: Dict[int, Dict] = {}
websocket_connections: Dict[str, WebSocket] = {}

class Order(BaseModel):
    id: int
    petId: int
    quantity: int
    shipDate: datetime.datetime
    status: str
    complete: bool

async def random_delay():
    delay = random.uniform(0.1, 1)
    await asyncio.sleep(delay)

@app.post("/api/v3/store/order")
async def create_order(order: Order):
    await random_delay()
    order_dict = order.dict()
    orders_db[order_dict["id"]] = order_dict
    await notify_clients(f"Order created: {order_dict['id']}")
    return orders_db[order_dict["id"]]

@app.get("/api/v3/store/inventory")
async def get_inventory():
    await random_delay()
    inventory = {}
    for order_id, order in orders_db.items():
        pet_id = order["petId"]
        quantity = order["quantity"]
        if pet_id not in inventory:
            inventory[pet_id] = 0
        inventory[pet_id] += quantity
    return inventory

@app.delete("/api/v3/store/order/{order_id}")
async def delete_order(order_id: int):
    await random_delay()
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    del orders_db[order_id]
    await notify_clients(f"Order deleted: {order_id}")
    return {"message": "Order deleted"}

@app.get("/api/v3/store/order/{order_id}")
async def get_order(order_id: int):
    await random_delay()
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders_db[order_id]

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(client_id: str, websocket: WebSocket):
    await websocket.accept()
    websocket_connections[client_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message received: {data}")
    except Exception as e:
        print(f"WebSocket error for client {client_id}: {str(e)}")
    finally:
        del websocket_connections[client_id]

async def notify_clients(message: str):
    for websocket in websocket_connections.values():
        await websocket.send_text(message)
