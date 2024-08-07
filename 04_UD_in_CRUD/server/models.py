from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
import re

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


class Production(db.Model, SerializerMixin):
    __tablename__ = "productions"
    __table_args__ = (
        db.CheckConstraint("budget >= 0 AND budget < 1000000", name="check_positive_budget_less_than_one_million"),
        db.UniqueConstraint("title", "director", name="uq_title_per_director"),
    )
    

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column("title", db.String(80), nullable=False, unique=True)
    genre = db.Column(db.String, nullable=False)
    director = db.Column(db.String)
    description = db.Column(db.String)
    budget = db.Column(db.Float)
    image = db.Column(db.String)
    ongoing = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    crew_members = db.relationship("CrewMember", back_populates="production", cascade="all, delete-orphan")

    # serialize_rules = ("-crew_members.production",)
    serialize_only = (
        "id",
        "title",
        "genre",
        "director",
        "description",
        "budget",
        "image",
        "ongoing",
        "created_at",
        "updated_at",
    )

    def __repr__(self):
        return f"""
            <Production #{self.id}:
                Title: {self.title}
                Genre: {self.genre}
                Director: {self.director}
        """

    # @property
    # def title(self):
    #     return self._title

    # @title.setter
    # def title(self, new_title):
    #     if not isinstance(new_title, str):
    #         raise TypeError('Titles must be of type str')
    #     elif not new_title:
    #         raise ValueError("Titles must have a length")
    #     self._title = new_title

    @validates("title", "description")
    def validate_title(self, key, value):
        if not isinstance(value, str):
            raise TypeError(f'{key.title()}s must be of type str')
        elif not value:
            raise ValueError(f"{key.title()}s must have a length")
        return value

    @validates("genre")
    def validate_genre(self, _, value):
        if not isinstance(value, str):
            raise TypeError(f"Genres must be of type str")
        elif value.title() not in ["Drama", "Musical", "Opera"]:
            raise ValueError("Genres must be one of Drama, Musical, Opera")
        return value

    @validates("image")
    def validate_image(self, _, value):
        if not isinstance(value, str):
            raise TypeError(f"Images must be of type str")
        elif not re.match(r"^https?:\/\/.*\.(?:jpeg|jpg|png)$", value):
            raise ValueError("Images must be of type jpeg, jpg, png")
        return value

    # def as_dict(self):
    #     return {
    #         "id": self.id,
    #         "title": self.title,
    #         "genre": self.genre,
    #         "director": self.director,
    #         "description": self.description,
    #         "budget": self.budget,
    #         "image": self.image,
    #         "ongoing": self.ongoing,
    #     }


class CrewMember(db.Model, SerializerMixin):
    __tablename__ = "crew_members"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    role = db.Column(db.String)
    production_id = db.Column(db.Integer, db.ForeignKey("productions.id"), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    production = db.relationship("Production", back_populates="crew_members")

    # serialize_rules = (
    #     "-production.crew_members",
    #     "-production.created_at",
    #     "-production.updated_at",
    # )
    serialize_only = ("id", "name", "role", "production_id", "created_at", "updated_at")
    # serialize_rules = ("-production",)

    def __repr__(self):
        return f"""
            <CrewMember #{self.id}:
                Name: {self.name}
                Role: {self.role}
                Production ID: {self.production_id}
        """
