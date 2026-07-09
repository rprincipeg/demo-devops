# Gestor de Tareas (To-Do API)

API REST sencilla construida con **Flask** que permite **crear, listar y eliminar tareas**.
El proyecto está pensado como un caso práctico que recorre **todo el ciclo DevOps**
(Plan → Crear → Paquete → Verificar → Lanzamiento → Configurar → Monitoreo) de forma
simple y fácil de explicar en una demo en vivo.

> **Historia de usuario:** Como usuario quiero crear, listar y eliminar tareas
> mediante una API REST.

El almacenamiento es **en memoria** (una lista de Python), por lo que los datos se
pierden al reiniciar la aplicación. Es suficiente para la demostración y evita la
complejidad de una base de datos.

---

## 📋 ¿Qué hace la API?

Cada tarea tiene la siguiente estructura:

```json
{
  "id": 1,
  "titulo": "Comprar pan",
  "completada": false
}
```

### Endpoints

| Método   | Ruta            | Descripción                                   | Respuestas                     |
|----------|-----------------|-----------------------------------------------|--------------------------------|
| `GET`    | `/health`       | Estado del servicio (para monitoreo)          | `200 OK`                       |
| `GET`    | `/tareas`       | Lista todas las tareas                        | `200 OK`                       |
| `POST`   | `/tareas`       | Crea una tarea (requiere campo `titulo`)      | `201 Created` / `400 Bad Request` |
| `DELETE` | `/tareas/<id>`  | Elimina la tarea por su `id`                  | `200 OK` / `404 Not Found`     |

### Ejemplos con `curl`

```bash
# Comprobar el estado del servicio
curl http://localhost:5000/health
# -> {"status": "ok"}

# Crear una tarea
curl -X POST http://localhost:5000/tareas \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Comprar pan"}'
# -> {"id": 1, "titulo": "Comprar pan", "completada": false}

# Intentar crear una tarea sin título (error de validación)
curl -X POST http://localhost:5000/tareas \
  -H "Content-Type: application/json" \
  -d '{}'
# -> {"error": "El campo 'titulo' es obligatorio"}  (status 400)

# Listar todas las tareas
curl http://localhost:5000/tareas
# -> [{"id": 1, "titulo": "Comprar pan", "completada": false}]

# Eliminar la tarea con id 1
curl -X DELETE http://localhost:5000/tareas/1
# -> {"mensaje": "Tarea eliminada"}

# Eliminar una tarea que no existe
curl -X DELETE http://localhost:5000/tareas/999
# -> {"error": "Tarea no encontrada"}  (status 404)
```

---

## 💻 Cómo correr localmente

Necesitas **Python 3.11** (o superior).

```bash
# 1. Crear y activar un entorno virtual
python -m venv .venv

# En Linux / macOS:
source .venv/bin/activate
# En Windows (PowerShell):
.venv\Scripts\Activate.ps1

# 2. Instalar las dependencias
pip install -r requirements.txt

# 3. Ejecutar la aplicación
flask --app app run --host 0.0.0.0 --port 5000
# (alternativa: python app.py)
```

La API quedará disponible en `http://localhost:5000`.

---

## ✅ Cómo correr los tests

Las pruebas están escritas con **pytest**:

```bash
pytest -v
```

Se ejecutan 6 pruebas que cubren: crear una tarea, listarlas, validar el error
sin título, eliminar una tarea existente, eliminar una inexistente y el endpoint
de salud.

---

## 🐳 Cómo construir y correr con Docker

```bash
# Construir la imagen
docker build -t gestor-tareas .

# Ejecutar el contenedor (mapeando el puerto 5000)
docker run -d -p 5000:5000 --name gestor-tareas gestor-tareas

# Probar
curl http://localhost:5000/health
```

Dentro del contenedor la aplicación se sirve con **gunicorn**, un servidor WSGI
apto para producción.

---

## 🔄 Ciclo DevOps cubierto por este proyecto

Este repositorio recorre las **7 etapas** del ciclo DevOps. Cada etapa se
corresponde con un archivo o mecanismo concreto:

```
   ┌──────────┐   ┌────────┐   ┌──────────┐   ┌───────────┐
   │  1. Plan │ → │2. Crear│ → │3. Paquete│ → │4. Verificar│
   └──────────┘   └────────┘   └──────────┘   └───────────┘
                                                     │
   ┌──────────────┐   ┌─────────────┐   ┌────────────▼───┐
   │ 7. Monitoreo │ ← │6. Configurar│ ← │ 5. Lanzamiento │
   └──────────────┘   └─────────────┘   └────────────────┘
```

| # | Etapa           | ¿Qué se hace?                                              | Archivo / Mecanismo                          |
|---|-----------------|------------------------------------------------------------|----------------------------------------------|
| 1 | **Plan**        | Definir la historia de usuario y los endpoints             | Este `README.md` (historia de usuario)       |
| 2 | **Crear**       | Escribir el código de la API                               | `app.py`                                      |
| 3 | **Paquete**     | Empaquetar la aplicación en una imagen Docker              | `Dockerfile` + job `build` del pipeline       |
| 4 | **Verificar**   | Ejecutar las pruebas automáticas                           | `test_app.py` + job `test` del pipeline       |
| 5 | **Lanzamiento** | Publicar la imagen en un registro de contenedores          | Job `push` → `ghcr.io` (GitHub Container Registry) |
| 6 | **Configurar**  | Desplegar el servicio en un entorno accesible              | Despliegue manual en Render/Railway (ver abajo) |
| 7 | **Monitoreo**   | Vigilar que el servicio siga disponible                    | Endpoint `/health` + UptimeRobot (ver abajo)  |

### Automatización (CI/CD)

Las etapas 3, 4 y 5 están automatizadas en el pipeline
[`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml), que se dispara con
cada `push` a la rama `main`:

```
push a main → [ test ] → [ build ] → [ push a ghcr.io ]
              (pytest)   (docker)    (imagen publicada)
```

Cada job depende del anterior: si las pruebas fallan, no se construye la imagen;
si el build falla, no se publica.

### 📝 Nota sobre Configurar y Monitoreo (pasos manuales)

- **Configurar (despliegue):** el despliegue final se realiza **manualmente** en
  [Render](https://render.com) o [Railway](https://railway.app) conectando este
  repositorio de GitHub. La plataforma detecta el `Dockerfile` (o el comando de
  gunicorn) y levanta el servicio automáticamente con cada cambio.
- **Monitoreo:** se configura [UptimeRobot](https://uptimerobot.com) apuntando al
  endpoint `/health` de la URL pública que entregue Render/Railway. UptimeRobot
  consulta ese endpoint periódicamente y avisa si el servicio deja de responder.

---

## 📁 Estructura del proyecto

```
.
├── app.py                     # Código de la API (Flask)
├── test_app.py                # Pruebas automáticas (pytest)
├── requirements.txt           # Dependencias de Python
├── Dockerfile                 # Definición de la imagen Docker
├── .github/workflows/ci-cd.yml # Pipeline CI/CD (GitHub Actions)
└── README.md                  # Este archivo
```
