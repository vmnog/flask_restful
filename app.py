from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
  def get(self, name):
    item = next(filter(lambda x: x['name'] == name, items), None) # 'next' returns a list if necessary or None
    return {'item': item}, 200 if item else 404 # returns 404 if item is None, otherwise return the item

  def post(self, name):
    if next(filter(lambda x: x['name'] == name, items), None): #if exits an item with the passed name 
      return {'message': "Item {} already exists.".format(name)}, 400

    data = request.get_json()
    item = {'name': name, 'price': data['price']}
    items.append(item)
    return item, 201

class ItemList(Resource):
  def get(self):
    return {'items': items}


# Tells API Student class will be accessible via API
api.add_resource(Item, '/item/<string:name>') #  http://localhost:3333/student/Victor
api.add_resource(ItemList, '/items')

app.run(port=3333, debug=True)