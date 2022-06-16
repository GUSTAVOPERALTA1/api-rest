from fastapi.testclient import TestClient
from code.main import app

clientes = TestClient(app)

def test_index():
    response = clientes.get("/")
    data = { "message":"API-REST" }
    assert response.status_code == 200
    assert response.json() == data