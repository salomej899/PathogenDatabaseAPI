from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.pathogens import PathogenModel


class PathogenList(Resource):

    def get(self):
        data = PathogenModel.get_all()
        if not data:
            return {"message": "მონაცემები არ არსებობს"}, 404
        pathogen_list = list(map(lambda pathogen: pathogen.json(), data))
        return {"pathogens": pathogen_list}, 200

    @jwt_required()
    def delete(self):
        try:
            PathogenModel.delete_all()
        except:
            return {"message": "დაფიქსირდა შეცდომა მონაცემების წაშლისას"}, 500
        return {"message": "მონაცემები წაიშალა"}, 200


class Pathogen(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("species",
                        type=str,
                        required=True,
                        help="საჭიროა სახეობის მითითება")

    parser.add_argument("strain",
                        type=str,
                        required=True,
                        help="საჭიროა შტამის მითითება")

    parser.add_argument("region",
                        type=str,
                        required=True,
                        help="საჭიროა რეგიონის მითითება")

    parser.add_argument("pathogen",
                        type=str,
                        required=True,
                        help="საჭიროა პათოგენის მითითება")

    parser.add_argument("sequence",
                        type=str)

    def get(self, name):
        item = PathogenModel.find_by_name(name)
        if not item:
            return {"message": f"{name} არ მოიძებნა"}, 400
        return item.json(), 200

    @jwt_required()
    def post(self, name):
        if PathogenModel.find_by_name(name):
            return {'message': f'მონაცემი {name} უკვე არსებობს'}, 400

        params = self.parser.parse_args()

        print(params)

        pathogen = PathogenModel(params["species"],
                                 params["strain"],
                                 params['pathogen'],
                                 params['region'],
                                 params['sequence'])

        try:
            pathogen.save_to_db()
        except:
            return {"message": "ინფორმაციის შენახვისას დაფიქსირდა შეცდომა"}, 500

        return {'message': f'მონაცემი {name} დამატებულია'}, 201

    @jwt_required()
    def put(self, name):
        params = self.parser.parse_args()
        strain = PathogenModel.find_by_name(name)
        if strain:
            strain.region = params['region']
            strain.sequence = params['sequence']
            message, code = f"მონაცემი {name} განახლებულია", 200

        else:
            strain = PathogenModelModel(**params)
            message, code = f"მონაცემი {name} დამატებულია", 201

        strain.save_to_db()

        return [{"message": message}, strain.json()], code

    @jwt_required()
    def delete(self, name):
        strain = PathogenModel.find_by_name(name)
        if strain:
            strain.delete_from_db()
            return {"message": f"მონაცემი {name} წაიშალა"}, 200
        return {"message": f"მონაცემი {name} არ მოიძებნა"}, 404
