from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
ARFLASK_PORT = 8081
ARMONGO_URL = "mongodb://localhost:27017/pythonmongodb"

ARapp = Flask(__name__)
ARapp.config["MONGO_URI"] = ARMONGO_URL
ARmongo = PyMongo(ARapp)

@ARapp.route(f'/tasks', methods=["GET"])
def get_tasks():
    ARrut = request.json['rut']
    ARexiste_rut = ARmongo.db.tasks.find_one({"rut": ARrut})

    if ARexiste_rut:
        ARtasks = ARmongo.db.tasks.aggregate([
            {"$match": {"rut": ARrut}},
            {"$unwind": "$tasks"},
            {"$replaceRoot": {"newRoot": "$tasks"}}
            ])
        ARlista_tareas = [ARtarea for ARtarea in ARtasks]
        return ARlista_tareas, 200

    else:
        return {'message': 'rut no encontrado'}, 404

@ARapp.route("/tasks", methods=["POST"])
def insert_task():
    # Receiving data
    ARrut = request.json['rut']
    ARnombreuser = request.json['nombreuser']
    ARcorreo = request.json['correo']
    ARtask = request.json['task']
    ARnombre = ARtask['nombre']

    ARexist_rut = ARmongo.db.tasks.find_one({'rut': ARrut}) 
    ARexist_task = ARmongo.db.tasks.find_one({"rut": ARrut, "tasks.nombre": ARnombre})
    # Si existe tarea no es posible ingresar
    if ARexist_task:
        return {'message': 'Ya existe una tarea con ese nombre'},400

    # Si existe el rut insertamos la tarea
    if ARexist_rut:
        ARmongo.db.tasks.update_one(
            {"rut": ARrut},
            {"$push": {"tasks": ARtask}}
            )
        return {'message': 'tarea insertada exitosamente'}, 200

    # Sino existe rut, creamos el rut he insertamos la tarea
    else:
        ARmongo.db.tasks.insert_one({
            'rut': ARrut,
            'nombreuser': ARnombreuser,
            'correo': ARcorreo,
            'tasks': [ARtask]
        })
        return {'message': 'rut creado y tarea insertada exitosamente'}, 200

@ARapp.route("/tasks", methods=["PUT"])
def update_task():
    # Recibe la información
    ARrut = request.json['rut']
    ARnombre = request.json['nombre']
    ARnew_task = request.json['new_task']

    ARexisten = ARmongo.db.tasks.find_one({"rut": ARrut, "tasks.nombre": ARnombre})
    if ARexisten:
        ARmongo.db.tasks.update_one(
            {"rut": ARrut, "tasks.nombre": ARnombre},  
            {"$set": {"tasks.$.nombre": ARnew_task['new_nombre'], 
                      "tasks.$.descripcion": ARnew_task['new_descripcion'],
                      "tasks.$.hecha": ARnew_task['new_hecha']}
                      })
        return {'message': 'tarea actualizada exitosamente'}, 200
    else:
        return {'message': 'el rut o tarea ingresada no existen'}, 404

@ARapp.route("/tasks", methods=["DELETE"])
def delete_task():
    # Recibe la información
    ARrut = request.json['rut']
    ARnombre = request.json['nombre']
    ARexisten = ARmongo.db.tasks.find_one({"rut": ARrut, "tasks.nombre": ARnombre})
    
    if ARexisten:
        ARmongo.db.tasks.update_one(
            {"rut": ARrut},
            {"$pull": {"tasks": {"nombre": ARnombre}}}
            )
        return {'message': 'tarea eliminada exitosamente'}, 200
    else:
        return {'message': 'el rut o tarea ingresada no existen'}, 404

@ARapp.route("/users", methods=["GET"])
def get_user():
    # Recibe la información del parámetro de consulta
    ARrut = request.args.get('rut')
    if ARrut is None:
        print("proporcion un rut")
        return {'message': 'proporcion un rut'}

    ARuser = ARmongo.db.tasks.find_one({"rut": ARrut})
    if ARuser:
        print("usuario encontrado")
        return {
            'rut': ARuser['rut'],
            'nombreuser': ARuser['nombreuser'],
            'correo': ARuser['correo']
        }, 200
    else:
        print("usuario no encontrado")
        return {'message': 'usuario no encontrado'}, 404
    
@ARapp.route("/users", methods=["POST"])  
def create_user():
    # Recive la información
    try:
        ARrut = request.json['rut']
        ARnombreuser = request.json['nombreuser']
        ARcorreo = request.json['correo']
    except:
        print("proporcion un rut, nombreuser y correo")
        return {'message': 'proporcion un rut, nombreuser y correo'}

    ARexist_user = ARmongo.db.tasks.find_one({"rut": ARrut})
    if ARexist_user:
        print("el usuario ya existe")
        return {'message':'el usuario ya existe'},400
    else:
        ARmongo.db.tasks.insert_one({
            'rut': ARrut,
            'nombreuser': ARnombreuser,
            'correo': ARcorreo,
            'tasks': []
        })
        print("usuario creado exitosamente")
        return {'message': 'usuario creado exitosamente'}, 200
        

if __name__ == "__main__":
    ARapp.run(debug=True, port=ARFLASK_PORT, host="0.0.0.0")
