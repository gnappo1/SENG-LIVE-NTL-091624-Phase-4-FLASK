from models.__init__ import SerializerMixin, db, validates, re
from app_config import flask_bcrypt
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, index=True, nullable=False)
    _password_hash = db.Column("password_hash", db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    serialize_rules = ("-_password_hash",)

    def __repr__(self):
        return f"User #{self.id}: {self.username}, {self.email}"

    @hybrid_property
    def password(self):
        raise AttributeError("passwords are private, set-only")

    @password.setter
    def password(self, password_to_validate):
        if not isinstance(password_to_validate, str):
            raise TypeError("password must be a string")
        if not 10 < len(password_to_validate) < 20:
            raise ValueError(
                "password must be a string between 10 and 20 characters long"
            )
        hashed_password = flask_bcrypt.generate_password_hash(
            password_to_validate
        ).decode("utf-8")
        self._password_hash = hashed_password

    def authenticate(self, password_to_check):
        return flask_bcrypt.check_password_hash(self._password_hash, password_to_check)

    @validates("username")
    def validate_username(self, _, username):
        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            raise ValueError("Username must be alphanumeric with underscores only")
        return username

    @validates("email")
    def validate_email(self, _, email):
        if not re.match(
            r"^(?:(?:[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+)*)|(?:'.+'))@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$",
            email,
        ):
            raise ValueError("Invalid email address")
        return email
