from db import db


class GuitarModel(db.Model):
    __tablename__ = 'guitars'

    id = db.Column(db.Integer, primary_key=True)
    guitar = db.Column(db.String, unique=True)
    price = db.Column(db.Float(precision=2))

    def __init__(self, guitar, price):
        self.guitar = guitar
        self.price = price

    def json(self):
        return {"guitar": self.guitar, "price": self.price}

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def delete_all(cls):
        cls.query.delete()
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(guitar=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
