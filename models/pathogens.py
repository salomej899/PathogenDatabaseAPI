from db import db


class PathogenModel(db.Model):
    __tablename__ = 'pathogens'

    id = db.Column(db.Integer, primary_key=True)
    species = db.Column(db.String)
    strain = db.Column(db.String, unique=True)
    pathogen = db.Column(db.String)
    sequence = db.Column(db.String)
    region = db.Column(db.String)
    # price = db.Column(db.Float(precision=2))

    def __init__(self, species, strain, pathogen, region, sequence):
        self.species = species
        self.strain = strain
        self.pathogen = pathogen
        self.sequence = sequence
        self.region = region

    def json(self):
        return {'species': self.species,
                "strain": self.strain,
                "pathogen": self.pathogen,
                'sequence': self.sequence,
                "region": self.region}

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def delete_all(cls):
        cls.query.delete()
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(strain=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
