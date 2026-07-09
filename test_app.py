"""
Pruebas automáticas (pytest) para la API Gestor de Tareas.

Estas pruebas verifican el comportamiento de cada endpoint. Se ejecutan
automáticamente en el pipeline de CI/CD (etapa "Verificar") antes de construir
y publicar la imagen Docker.
"""

import pytest

import app as app_modulo


@pytest.fixture
def cliente():
    """Crea un cliente de pruebas de Flask y reinicia el almacenamiento.

    Reiniciamos la lista de tareas antes de cada prueba para que sean
    independientes entre sí.
    """
    app_modulo.tareas.clear()
    app_modulo.siguiente_id = 1
    app_modulo.app.config["TESTING"] = True
    return app_modulo.app.test_client()


def test_crear_tarea(cliente):
    """Test 1: crear una tarea correctamente devuelve status 201."""
    respuesta = cliente.post("/tareas", json={"titulo": "Comprar pan"})
    assert respuesta.status_code == 201

    datos = respuesta.get_json()
    assert datos["titulo"] == "Comprar pan"
    assert datos["completada"] is False
    assert datos["id"] == 1


def test_listar_tareas(cliente):
    """Test 2: listar tareas devuelve status 200 y la estructura correcta."""
    cliente.post("/tareas", json={"titulo": "Estudiar DevOps"})

    respuesta = cliente.get("/tareas")
    assert respuesta.status_code == 200

    datos = respuesta.get_json()
    assert isinstance(datos, list)
    assert len(datos) == 1
    assert datos[0]["titulo"] == "Estudiar DevOps"


def test_crear_tarea_sin_titulo(cliente):
    """Test 3: crear una tarea sin el campo 'titulo' devuelve status 400."""
    respuesta = cliente.post("/tareas", json={})
    assert respuesta.status_code == 400


def test_eliminar_tarea_existente(cliente):
    """Test 4: eliminar una tarea existente devuelve status 200."""
    creacion = cliente.post("/tareas", json={"titulo": "Tarea a borrar"})
    tarea_id = creacion.get_json()["id"]

    respuesta = cliente.delete(f"/tareas/{tarea_id}")
    assert respuesta.status_code == 200


def test_eliminar_tarea_inexistente(cliente):
    """Test 5: eliminar una tarea inexistente devuelve status 404."""
    respuesta = cliente.delete("/tareas/999")
    assert respuesta.status_code == 404


def test_health(cliente):
    """Test 6: el endpoint de salud devuelve status 200 y estado 'ok'."""
    respuesta = cliente.get("/health")
    assert respuesta.status_code == 200
    assert respuesta.get_json() == {"status": "ok"}
