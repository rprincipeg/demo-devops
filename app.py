"""
Gestor de Tareas (To-Do API)
============================

API REST sencilla construida con Flask que permite crear, listar y eliminar
tareas. El almacenamiento es en memoria (una lista de Python), por lo que los
datos se pierden al reiniciar la aplicación.

Historia de usuario:
    Como usuario quiero crear, listar y eliminar tareas mediante una API REST.
"""

import os

from flask import Flask, jsonify, request

app = Flask(__name__)

# Almacenamiento en memoria: lista de tareas y un contador para los ids.
tareas = []
siguiente_id = 1


@app.route("/health", methods=["GET"])
def health():
    """Endpoint de salud usado para el monitoreo (por ejemplo, UptimeRobot)."""
    return jsonify({"status": "bien"}), 200


@app.route("/tareas", methods=["GET"])
def listar_tareas():
    """Devuelve la lista completa de tareas en formato JSON."""
    return jsonify(tareas), 200

def test_listar_tareas_vacia():
    response = client.get('/tareas')
    assert response.status_code == 200


@app.route("/tareas", methods=["POST"])
def crear_tarea():
    """Crea una nueva tarea a partir de un JSON con el campo 'Nombre'.

    Responde 400 si el campo 'NOmbre' no está presente.
    """
    global siguiente_id

    datos = request.get_json(silent=True) or {}

    # Validación: el campo 'Nombre' es obligatorio.
    if "Nombre" not in datos or not datos["Nombre"]:
        return jsonify({"error": "El campo 'Nombre' es obligatorio"}), 400

    tarea = {
        "id": siguiente_id,
        "Nombre": datos["Nombre"],
        "completada": False,  # Toda tarea nueva empieza sin completar.
    }
    tareas.append(tarea)
    siguiente_id += 1

    return jsonify(tarea), 201


@app.route("/tareas/<int:tarea_id>", methods=["DELETE"])
def eliminar_tarea(tarea_id):
    """Elimina la tarea con el id indicado.

    Responde 404 si no existe ninguna tarea con ese id.
    """
    for tarea in tareas:
        if tarea["id"] == tarea_id:
            tareas.remove(tarea)
            return jsonify({"mensaje": "Tarea eliminada"}), 200

    return jsonify({"error": "Tarea no encontrada"}), 404


if __name__ == "__main__":
    # Modo de desarrollo. En producción se usa gunicorn (ver Dockerfile).
    # Render inyecta la variable de entorno PORT; si no existe, usamos 5000.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

def test_tarea_creada_tiene_campos_correctos():
    """Verifica que al crear una tarea, la respuesta incluya id, Nombre y completada."""
    response = client.post('/tareas', json={"Nombre": "Preparar presentacion DevOps"})
    data = response.get_json()

    assert response.status_code == 201
    assert "id" in data
    assert data["Nombre"] == "Preparar presentacion DevOps"
    assert data["completada"] == False

def test_crear_tarea(cliente):
    """Test 1: crear una tarea correctamente devuelve status 201."""
    respuesta = cliente.post("/tareas", json={"titulo": "Comprar pan"})
    assert respuesta.status_code == 201

    datos = respuesta.get_json()
    assert datos["titulo"] == "Comprar pan"
    assert datos["completada"] is False
    assert datos["id"] == 1