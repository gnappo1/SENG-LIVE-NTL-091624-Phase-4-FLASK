from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

class Production(db.Model):
    __tablename__ = 'productions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    genre = db.Column(db.String, nullable=False)
    director = db.Column(db.String)
    description = db.Column(db.String)
    budget = db.Column(db.Float)
    image = db.Column(db.String)
    ongoing = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    crew_members = db.relationship("CrewMember", back_populates="production")

    def __repr__(self):
        return f"""
            <Production #{self.id}:
                Title: {self.title}
                Genre: {self.genre}
                Director: {self.director}
        """
    
    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "genre": self.genre,
            "director": self.director,
            "description": self.description,
            "budget": self.budget,
            "image": self.image,
            "ongoing": self.ongoing,
        }

class CrewMember(db.Model):
    __tablename__ = 'crew_members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    role = db.Column(db.String)
    production_id = db.Column(db.Integer, db.ForeignKey('productions.id'))

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    production = db.relationship("Production", back_populates="crew_members")
    def __repr__(self):
        return f"""
            <CrewMember #{self.id}:
                Name: {self.name}
                Role: {self.role}
                Production ID: {self.production_id}
        """
