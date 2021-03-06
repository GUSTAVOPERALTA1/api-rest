from fastapi.testclient import TestClient
from code.main import app

clientes = TestClient(app)

def test_index():
    response = clientes.get("/")
    data = { "message":"API-REST" }
    assert response.status_code == 200
    assert response.json() == data


def test_limit():
	response = clientes.get('/clientes/offset=0&limit=3')
	data = [{"id_cliente":1,"nombre":"Saul","email":"saul@gmail.com"},
	{"id_cliente":2,"nombre":"Maria","email":"maria@gmail.com"},
	{"id_cliente":3,"nombre":"Fatima","email":"fatima@gmail.com"}]
	assert response.status_code == 200
	assert response.json()==data