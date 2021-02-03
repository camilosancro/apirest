from flask import Flask, jsonify, request

app = Flask(__name__)

from products import products

@app.route('/ping')
def ping():
    return jsonify({"message":"pong!"})

@app.route('/products', methods=['GET'])
def getProducts():
    return jsonify({"products":products, "message":"Products list"})

@app.route('/products/<string:product_name>', methods=['GET'])
def getProduct(product_name):
    productFound = [product for product in products if product['name'] == product_name] 
    if (len(productFound) > 0):
        return jsonify({"product": productFound[0]})
    else:
        return jsonify("message:", "Producto no encontrado")

@app.route('/products', methods=['POST'])
def addProduct():
    new_product = {
        "name" : request.json['name'],
        "price" : request.json['price'],
        "quantity" : request.json['quantity'] 
    }
    products.append(new_product)
    return jsonify({"message:":"Producto ingresado correctamente","productos:": products})

@app.route('/products/<string:product_name>', methods=['PUT'])
def editProduct(product_name):
    productFound = [product for product in products if product['name'] == product_name] 
    if (len(productFound) > 0):
        productFound[0]['name'] = request.json['name']
        productFound[0]['price'] = request.json['price']
        productFound[0]['quantity'] = request.json['quantity']
        return jsonify({
            "message": "Producto actualizado",
            "product": productFound[0]
        })
    else:
        return jsonify("message:", "Producto no encontrado")


if __name__ == '__main__':
    app.run(debug=True, port=4000)


