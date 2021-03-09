from flask import Flask, redirect
from flask_restful import Api
from flask_jwt import JWT
from security import authentication, identity
from resources.users import RegisterUser
from resources.pathogens import PathogenList, Pathogen

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"

api = Api(app)

jwt = JWT(app, authentication, identity)


@app.route("/")
def home():
    return redirect("https://github.com/salomej899/GuitarStore_Rest_API/tree/main"), 302


api.add_resource(PathogenList, "/pathogens")
api.add_resource(Pathogen, '/pathogens/<string:name>')
api.add_resource(RegisterUser, '/registration')

if __name__ == "__main__":
    from db import db
    db.init_app(app)

    app.run(debug=True)
