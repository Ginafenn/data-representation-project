# Project


# Import packages
from flask import Flask, url_for, redirect,request, jsonify, abort
from PhonesDAO import phoneDAO
from flask import Flask
from flask_cors import CORS


app = Flask(__name__, static_url_path='', static_folder='staticpages')
CORS(app)

""" phones=[
    {"id": 1, "Make": "Samsung", "Model": "s20", "Price": 500},
    {"id": 2, "Make": "Samsung", "Model": "A21", "Price": 600},
    {"id": 3, "Make": "Samsung", "Model": "S23", "Price": 800}
]
nextId=4 """

@app.route('/')

def index():
        return "Phones"

@app.route('/phones', methods=['GET', 'POST'])

def getAll():
    results = phoneDAO.getAll()
    return jsonify(results)


# find By id
@app.route('/phones/<int:id>')
def findById(id):
    foundphone = phoneDAO.findByID(id)

    return jsonify(foundphone)

#curl -X POST -H "content-type:application/json" -d "{\"Make\":\"Samsung\", \"Model\":\"A54\", \"Price\":600}" http://127.0.0.1:5000/phones
# Create
@app.route('/phones', methods=['POST'])
def create():
    if not request.json or 'Make' not in request.json or 'Model' not in request.json or 'Price' not in request.json:
        abort(400)

    make = request.json['Make']
    model = request.json['Model']
    price = request.json['Price']

    # Perform validation on make, model, and price if needed

    new_id = phoneDAO.create(make, model, price)

    new_phone = {
        "id": new_id,
        "Make": make,
        "Model": model,
        "Price": price
    }

    return jsonify(new_phone)

#update
#curl -X PUT -d "{\"Make\":\"Nokia\", \"Model\":\"A54\", \"Price\":600}" -H "content-type:application/json" http://127.0.0.1:5000/phones/1
@app.route('/phones/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def update(id):

    foundphone = phoneDAO.findByID(id)

    if not foundphone:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'Price' in reqJson and type(reqJson['Price']) is not int:
        abort(400)

    if 'title' in reqJson:
        foundphone['Make'] = reqJson['Make']
    if 'Author' in reqJson:
        foundphone['Model'] = reqJson['Model']
    if 'price' in reqJson:
        foundphone['Price'] = reqJson['Price']
    values = (foundphone['Make'],foundphone['Model'],foundphone['Price'],foundphone['id'])
    phoneDAO.update(values)
    return jsonify(foundphone)


#delete
# curl -X DELETE http://127.0.0.1:5000/phones/1
@app.route('/phones/<int:id>', methods=['DELETE'])
def delete(id):
    phoneDAO.delete(id)
    return jsonify({"done":True})



if __name__ == "__main__":
    app.run(debug = True)

