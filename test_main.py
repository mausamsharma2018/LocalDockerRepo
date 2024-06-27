from fastapi.testclient import TestClient
from main import app, orders_db
from pydantic import BaseModel
import datetime

client = TestClient(app)

class Order(BaseModel):
    id: int
    petId: int
    quantity: int
    shipDate: datetime.datetime
    status: str
    complete: bool

def test_create_order():
    order = {
        "id": 144,
        "petId": 198772,
        "quantity": 90,
        "shipDate": "2024-06-22T14:02:51.092Z",
        "status": "approved",
        "complete": True
    }
    response = client.post("/api/v3/store/order", json=order)
    assert response.status_code == 200
    assert response.json()["id"] == 144
    assert 144 in orders_db

def test_get_inventory():
    response = client.get("/api/v3/store/inventory")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_delete_order():
    order_id = 144
    response = client.delete(f"/api/v3/store/order/{order_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Order deleted"
    assert order_id not in orders_db

def test_get_order():
    order_id = 144
    response = client.get(f"/api/v3/store/order/{order_id}")
    assert order_id not in orders_db
    assert response.status_code == 404

# Note: WebSocket testing can be more complex and might require specialized libraries or manual testing tools.
# The following is a basic example without actual WebSocket connection establishment.

def test_websocket():
    with client.websocket_connect("/ws/client1") as websocket:
        websocket.send_text("Hello")
        data = websocket.receive_text()
        assert data == "Message received: Hello"
