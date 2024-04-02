from flask import Flask, request
from flask_pymongo import PyMongo

FLASK_PORT = 8081
MONGO_URL = "mongodb://localhost:27017/pythonmongodb"

app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URL
mongo = PyMongo(app)

@app.route("/users", methods=["POST"])
def create_user():
    # Receiving data
    rut = request.json['rut']

    if rut:
        id = mongo.db.users.insert(
            {'rut': rut}
            )
        response = {
            'id': str(id),
            'rut': rut,
        }
        return response
    else:
        pass
    
    

if __name__ == "__main__":
    app.run(debug=True, port=FLASK_PORT)  