from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field can not be left blank"
        )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store_id"
        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return{"message":"Item not found"},404

    def post(self,name):#first checks to see that name is unique before adding it to data
        if ItemModel.find_by_name(name):
            return{"message":"an item with this name'{}' already exists".format(name)},400

        data=Item.parser.parse_args()
        item=ItemModel(name, **data)#uses the price key to retrieve the price from the data dictionary

        try:
            item.save_to_db()
        except:
            return{"message":"An internal server error occurred"},500

        return item.json()

    def delete(self,name):
        item=ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return{"Message":"Item Deleted"}

    def put(self,name):
        data=Item.parser.parse_args()

        item=ItemModel.find_by_name(name)

        if item is None:
            item=ItemModel(name, data['price'], data['store_id'])
        else:
            item.price=data['price']

        item.save_to_db()

        return item.json()


class Itemlist(Resource):
    def get(self):

        return {'items': [item.json() for item in ItemModel.find_all()]}
