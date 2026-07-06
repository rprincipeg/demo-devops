from app import app

def test_home():
    cliente = app.test_client()
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200
    assert respuesta.get_json()["mensaje"] == "Hola, DevOps!"

def test_salud():
    cliente = app.test_client()
    respuesta = cliente.get("/salud")
    assert respuesta.status_code == 200
