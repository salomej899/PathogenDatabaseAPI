from flask_restful import reqparse, Resource
from models.users import UserModel


class RegisterUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="საჭიროა 'username'-ის მითითება")

    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="საჭიროა 'password'-ის მითითება")

    def post(self):
        params = self.parser.parse_args()
        username = params["username"]
        if UserModel.find_by_username(username):
            return {"message": f"მომხმარებელი {username} უკვე არსებობს"}, 400
        password = params["password"]
        user = UserModel(username, password)
        try:
            user.save_to_db()
        except:
            return {"message": "ინფორმაციის შენახვისას დაფიქსირდა შეცდომა"}, 500
        return {"message": f"მომხმარებელი {username} დარეგისტრირებულია"}, 201
