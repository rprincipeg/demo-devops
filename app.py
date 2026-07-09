"""
Gestor de Tareas (To-Do API)
============================

API REST sencilla construida con Flask que permite crear, listar y eliminar
tareas. El almacenamiento es en memoria (una lista de Python), por lo que los
datos se pierden al reiniciar la aplicación. Esto es suficiente para una demo
del ciclo DevOps y mantiene el código simple y fácil de explicar.

Historia de usuario:
    Como usuario quiero crear, listar y eliminar tareas mediante una API REST.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

# Almacenamiento en memoria: lista de tareas y un contador para los ids.
tareas = []
siguiente_id = 1


@app.route("/health", methods=["GET"])
def health():
    """Endpoint de salud usado para el monitoreo (por ejemplo, UptimeRobot)."""
    return jsonify({"status": "ok"}), 200


@app.route("/tareas", methods=["GET"])
def listar_tareas():
    """Devuelve la lista completa de tareas en formato JSON."""
    return jsonify(tareas), 200


@app.route("/tareas", methods=["POST"])
def crear_tarea():
    """Crea una nueva tarea a partir de un JSON con el campo 'titulo'.

    Responde 400 si el campo 'titulo' no está presente.
    """
    global siguiente_id

    datos = request.get_json(silent=True) or {}

    # Validación: el campo 'titulo' es obligatorio.
    if "titulo" not in datos or not datos["titulo"]:
        return jsonify({"error": "El campo 'titulo' es obligatorio"}), 400

    tarea = {
        "id": siguiente_id,
        "titulo": datos["titulo"],
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
    app.run(host="0.0.0.0", port=5000, debug=True)
