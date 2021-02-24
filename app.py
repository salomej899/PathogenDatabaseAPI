from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authentication, identity
from resources.users import RegisterUser
from resources.guitars import GuitarList, Guitar

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"

api = Api(app)

jwt = JWT(app, authentication, identity)

@app.before_first_request
def create_table():
    db.create_all()

api.add_resource(GuitarList, "/guitars")
api.add_resource(Guitar, '/guitars/<string:name>')
api.add_resource(RegisterUser, '/registration')

if __name__ == "__main__":
    from db import db
    db.init_app(app)

    app.run(debug=True)
