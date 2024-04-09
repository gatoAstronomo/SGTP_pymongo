from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
FLASK_PORT = 8081
MONGO_URL = "mongodb://localhost:27017/pythonmongodb"

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URL
mongo = PyMongo(app)

@app.route(f'/tasks', methods=["GET"])
def get_task():
    rut = request.json['rut']
    if not rut:
        return {'message': 'Proporcione un rut'}

    
@app.route("/tasks", methods=["POST"])
def insert_task():
    # Receiving data
    rut = request.json['rut']
    task = request.json['task']
    if not rut:
        return {'message': 'Proporcione un rut'}

    # Si existe el rut en la db actualizamos las tareas de ese rut
    exist_rut = mongo.db.tasks.find_one({'rut': rut}) 
    if exist_rut:
        id = mongo.db.tasks.update_one(
            {"rut": rut},
            {"$push": {"tasks": task}}
            )
        return {'message': 'tarea insertada exitosamente'}

    # Sino existe lo creamos
    else:
        mongo.db.tasks.insert_one({
            'rut': rut,
            'tasks': [task]
        })
        return {'message': 'rut creado y tarea insertada exitosamente'}

@app.route("/tasks", methods=["PUT"])
def update_task():
    # Recibe la información
    rut = request.json['rut']
    nombre = request.json['nombre']
    new_task = request.json['new_task']

    existen = mongo.db.tasks.find_one({"rut": rut, "tasks.nombre": nombre})
    if existen:
        mongo.db.tasks.update_one(
            {"rut": rut, "tasks.nombre": nombre},  
            {"$set": {"tasks.$.nombre": new_task['new_nombre'], 
                      "tasks.$.descripcion": new_task['new_descripcion'],
                      "tasks.$.hecha": new_task['new_hecha']}
                      })
        return {'message': 'tarea actualizada exitosamente'}
    else:
        return {'message': 'el rut o tarea ingresada no existen'}
    

if __name__ == "__main__":
    app.run(debug=True, port=FLASK_PORT, host="0.0.0.0")  