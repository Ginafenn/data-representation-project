# Project

# Import packages
from flask import Flask, url_for, redirect,request, jsonify, abort
from PhonesDAO import phoneDAO
from flask_cors import CORS
import logging

logging.basicConfig(level=logging.DEBUG)


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

# Create
@app.route('/phones', methods=['POST'])
def create():

    if not request.json:
        abort(400)
    # Checking 
    phone = {
        "Make": request.json['Make'],
        "Model": request.json['Model'],
        "Price": request.json['Price'],
    }
    values =(phone['Make'],phone['Model'],phone['Price'])

    new_id = phoneDAO.create(values)
    if new_id is not None:
        
        phone['id'] = new_id
        logging.debug(f"New phone created with ID: {new_id}")
        return jsonify(phone), 201
    else:
        logging.error("Failed to create phone")
        return jsonify({"error": "Failed to create phone"}), 500
    

# update
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

    if 'Make' in reqJson:
        foundphone['Make'] = reqJson['Make']
    if 'Model' in reqJson:
        foundphone['Model'] = reqJson['Model']
    if 'Price' in reqJson:
        foundphone['Price'] = reqJson['Price']
    values = (foundphone['Make'],foundphone['Model'],foundphone['Price'],foundphone['id'])
    phoneDAO.update(values)
    return jsonify(foundphone)


#delete
@app.route('/phones/<int:id>', methods=['DELETE'])
def delete(id):
    phoneDAO.delete(id)
    return jsonify({"done":True})



if __name__ == "__main__":
    app.run(debug = True)

