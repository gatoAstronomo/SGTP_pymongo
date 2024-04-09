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

    # Revisa si existe el rut en la base de datos
    exist_rut = mongo.db.tasks.find_one({'rut': rut}) 
    if not exist_rut:
        id = mongo.db.tasks.insert_one(
            {
                'rut': rut,
                'task': task
                }
        )
        response = {
            'id': str(id.inserted_id),
            'rut': rut,
            'task': task
        }
        return response

    else:
        return {'message': 'El rut ya existe'}
    

if __name__ == "__main__":
    app.run(debug=True, port=FLASK_PORT, host="0.0.0.0")  