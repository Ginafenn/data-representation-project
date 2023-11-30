from flask import Flask, url_for, redirect,request, jsonify, abort

app = Flask(__name__, static_url_path='', static_folder='staticpages')

phones=[
    {"id": 1, "Make": "Samsung", "Model": "s20", "Price": 500},
    {"id": 2, "Make": "Samsung", "Model": "A21", "Price": 600},
    {"id": 3, "Make": "Samsung", "Model": "S23", "Price": 800}
]
nextId=4

@app.route('/')

def index():
        return "Hello World"

@app.route('/phones')
def getAll():
    return jsonify(phones)


# find By id
@app.route('/phones/<int:id>')
def findById(id):
        foundPhones = list(filter (lambda t : t["id"]== id, phones))
        if len(foundPhones) == 0:
            return jsonify({}) , 204
        return jsonify(foundPhones[0])

#curl -X POST -H "content-type:application/json" -d "{\"Make\":\"Samsung\", \"Model\":\"A54\", \"Price\":600}" http://127.0.0.1:5000/phones
# Create
@app.route('/phones', methods=['POST'])
def create():
    global nextId
    if not request.json:
        abort(400)

    
    phone = {
        "id": nextId,
        "Make": request.json["Make"],
        "Model": request.json["Model"],
        "Price": request.json["Price"]
    }
    phones.append(phone)
    nextId += 1
    return jsonify(phone)



#update
#curl -X PUT -d "{\"Make\":\"Nokia\", \"Model\":\"A54\", \"Price\":600}" -H "content-type:application/json" http://127.0.0.1:5000/phones/1
@app.route('/phones/<int:id>', methods=['PUT'])
def update(id):
    foundPhones = list(filter(lambda t: t["id"] == id, phones))
    if len(foundPhones) == 0:
        return jsonify({}), 404
    currentphone = foundPhones[0]
    if 'Make' in request.json:
        currentphone['Make'] = request.json['Make']
    if 'Model' in request.json:
        currentphone['Model'] = request.json['Model']
    if 'Price' in request.json:
        currentphone['Price'] = request.json['Price']

    return jsonify(currentphone)


#delete
# curl -X DELETE http://127.0.0.1:5000/phones/1
@app.route('/phones/<int:id>', methods=['DELETE'])
def delete(id):
    foundPhones = list(filter(lambda t: t["id"] == id, phones))
    if len(foundPhones) == 0:
        return jsonify({}), 404
    phones.remove(foundPhones[0])

    return jsonify({"done":True})



if __name__ == "__main__":
    app.run(debug = True)

if __name__ == "__main__":
    app.run(debug=True)