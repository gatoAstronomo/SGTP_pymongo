from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
FLASK_PORT = 8081
MONGO_URL = "mongodb://localhost:27017/pythonmongodb"

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URL
mongo = PyMongo(app)

@app.route(f'/tasks', methods=["GET"])
def get_tasks():
    rut = request.json['rut']
    existe_rut = mongo.db.tasks.find_one({"rut": rut})

    if existe_rut:
        tasks = mongo.db.tasks.aggregate([
            {"$match": {"rut": rut}},
            {"$unwind": "$tareas"},
            {"$replaceRoot": {"newRoot": "$tareas"}}
            ])
        lista_tareas = [tarea for tarea in tasks]
        return lista_tareas, 200

    else:
        return {'message': 'rut no encontrado'}, 404


    
@app.route("/tasks", methods=["POST"])
def insert_task():
    # Receiving data
    rut = request.json['rut']
    task = request.json['task']
    if not rut:
        return {'message': 'Proporcione un rut'}, 400

    # Si existe el rut en la db actualizamos las tareas de ese rut
    exist_rut = mongo.db.tasks.find_one({'rut': rut}) 
    if exist_rut:
        id = mongo.db.tasks.update_one(
            {"rut": rut},
            {"$push": {"tasks": task}}
            )
        return {'message': 'tarea insertada exitosamente'}, 200

    # Sino existe lo creamos
    else:
        mongo.db.tasks.insert_one({
            'rut': rut,
            'tasks': [task]
        })
        return {'message': 'rut creado y tarea insertada exitosamente'}, 200

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
        return {'message': 'tarea actualizada exitosamente'}, 200
    else:
        return {'message': 'el rut o tarea ingresada no existen'}, 404

@app.route("/tasks", methods=["DELETE"])
def delete_task():
    # Recibe la información
    rut = request.json['rut']
    nombre = request.json['nombre']
    existe = mongo.db.tasks.find_one({"rut": rut, "tasks.nombre": nombre})
    
    if existen:
        mongo.db.tasks.update_one(
            {"rut": rut},
            {"$pull": {"tasks": {"nombre": nombre}}}
            )
        return {'message': 'tarea eliminada exitosamente'}, 200
    else:
        return {'message': 'el rut o tarea ingresada no existen'}, 404
    
@app.route("/ruts", methods=["GET"])
def existe_rut():
    rut = request.json['rut']
    exist_rut = mongo.db.tasks.find_one({'rut': rut}) 
    if exist_rut:
        return {'message': 'el rut existe en la db'}, 200
    else:
        return {'message': 'el rut no fue encontrado'}, 400
        


if __name__ == "__main__":
    app.run(debug=True, port=FLASK_PORT, host="0.0.0.0")  