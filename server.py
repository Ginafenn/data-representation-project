from flask import Flask, url_for, redirect,request, jsonify, abort

from PhonesDAO import phoneDAO

app = Flask(__name__, static_url_path='', static_folder='staticpages')

""" phones=[
    {"id": 1, "Make": "Samsung", "Model": "s20", "Price": 500},
    {"id": 2, "Make": "Samsung", "Model": "A21", "Price": 600},
    {"id": 3, "Make": "Samsung", "Model": "S23", "Price": 800}
]
nextId=4 """

@app.route('/')

def index():
        return "Hello World"

@app.route('/phones')
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

    if not request.json:
        abort(400)

    phone = {
        "Make": request.json["Make"],
        "Model": request.json["Model"],
        "Price": request.json["Price"]
    }
    values =(phone['Make'],phone['Model'],phone['Price'])
    newId = phoneDAO.create(values)
    phone['id'] = newId
    return jsonify(phone)



#update
#curl -X PUT -d "{\"Make\":\"Nokia\", \"Model\":\"A54\", \"Price\":600}" -H "content-type:application/json" http://127.0.0.1:5000/phones/1
@app.route('/phones/<int:id>', methods=['PUT'])
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

