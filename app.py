from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []


class Item(Resource):
    @jwt_required()  # makes get methods/routes jwt required
    def get(self, name):
        # 'next' returns a list if necessary or None
        item = next(filter(lambda x: x['name'] == name, items), None)
        # returns 404 if item is None, otherwise return the item
        return {'item': item}, 200 if item else 404

    def post(self, name):
        # if exits an item with the passed name
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "Item {} already exists.".format(name)}, 400

        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items  # forces that items var is the item list we declared @ 12l
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):  # creates or updates if doesn't exists
        data = request.get_json()
        # return if find or None if dont
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}


# Tells API Student class will be accessible via API
# http://localhost:3333/student/Victor
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=3333, debug=True)
