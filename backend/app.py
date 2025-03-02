from flask import Flask, request, jsonify
from database import db 


def create_app():
    app = Flask(__name__)

    # Configura la base de datos SQLite
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///backend/tasks.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)  # Inicializa db aquí

    from models import Task  # Mueve la importación aquí, después de la inicialización de db

    @app.route("/")
    def hello_world():
        return "Hola, mundo"

    # Ruta para crear una tarea (CREATE)
    @app.route("/tasks", methods=["POST"])
    def create_task():
        data = request.get_json()  # Obtiene los datos del cuerpo de la solicitud
        new_task = Task(
            title=data["title"],
            description=data["description"],
            completed=data.get("completed", False)
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message": "Tarea creada", "task": {"id": new_task.id, "title": new_task.title}}), 201

    # Ruta para obtener las tareas (READ)
    @app.route("/tasks", methods=["GET"])
    def get_tasks():
        tasks = Task.query.all()
        task_list = []
        for task in tasks:
            task_list.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            })
        return jsonify(task_list)

    # Ruta para traer una tarea específica
    @app.route("/tasks/<int:id>", methods=["GET"])
    def get_task(id):
        task = Task.query.get_or_404(id)
        return jsonify({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        })

    # Ruta para actualizar una tarea (UPDATE)
    @app.route("/tasks/<int:id>", methods=["PUT"])
    def update_task(id):
        task = Task.query.get_or_404(id)
        data = request.get_json()
        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        task.completed = data.get("completed", task.completed)
        db.session.commit()
        return jsonify({"message": "Tarea actualizada", "task": {"id": task.id, "title": task.title}})

    # Ruta para eliminar una tarea (DELETE)
    @app.route("/tasks/<int:id>", methods=["DELETE"])
    def delete_task(id):
        task = Task.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Tarea eliminada"})

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)