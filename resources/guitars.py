from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.guitars import GuitarModel


class GuitarList(Resource):

    def get(self):
        data = GuitarModel.get_all()
        if not data:
            return {"message": "მონაცემები არ არსებობს"}, 404

        guitar_list = []
        for i in range(len(data)):
            guitar = GuitarModel.json(data[i])
            guitar_list.append(guitar)
        return guitar_list, 200

    @jwt_required()
    def delete(self):
        try:
            GuitarModel.delete_all()
        except:
            return {"message": "დაფიქსირდა შეცდომა მონაცემების წაშლისას"}, 500
        return {"message": "მონაცემები წაიშალა"}, 200


class Guitar(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("guitar",
                        type=str,
                        required=True,
                        help="საჭიროა გიტარის მითითება")

    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="საჭიროა 'price'-ის მითითება")

    def get(self, name):
        item = GuitarModel.find_by_name(name)
        if not item:
            return {"message": f"პროდუქტი {name} არ მოიძებნა"}, 400
        return item.json(), 200

    @jwt_required()
    def post(self, name):
        if GuitarModel.find_by_name(name):
            return {'message': f'მონაცემი {name} უკვე არსებობს'}, 400

        params = self.parser.parse_args()

        guitar = GuitarModel(params["guitar"], params["price"])

        try:
            guitar.save_to_db()
        except:
            return {"message": "ინფორმაციის შენახვისას დაფიქსირდა შეცდომა"}, 500

        return {'message': f'მონაცემი {name} დამატებულია'}, 201

    @jwt_required()
    def put(self, name):
        params = self.parser.parse_args()
        guitar = GuitarModel.find_by_name(name)
        if guitar:
            guitar.price = params["price"]
            message, code = f"მონაცემი {name} განახლებულია", 200

        else:
            guitar = GuitarModel(**params)
            message, code = f"მონაცემი {name} დამატებულია", 201

        guitar.save_to_db()

        return [{"message": message}, guitar.json()], code

    @jwt_required()
    def delete(self, name):
        guitar = GuitarModel.find_by_name(name)
        if guitar:
            guitar.delete_from_db()
            return {"message": f"მონაცემი {name} წაიშალა"}, 200
        return {"message": f"მონაცემი {name} არ მოიძებნა"}, 404
