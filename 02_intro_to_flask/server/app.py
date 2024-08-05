from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from models import db, Production, CrewMember

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///theater.db"

#! Ideal configuration for all your apps
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#! Set up the connection between app and db for alembic - MIGRATION VERSION CONTROL
migrate = Migrate(app, db)
#! Set up the connection between app and db for SQLAlchemy
db.init_app(app)

@app.route("/")
def homepage():
    return "Hello World!"

@app.route("/productions", methods=["GET", "POST"])
def productions():
    if request.method == "GET":
        try:
            #! return a list of dictionaries representing the productions
            #! INSTEAD OF A LIST OF Production objects
            prods = [prod.as_dict() for prod in Production.query.all()]
            # return make_response(prods, 200, {})
            # return jsonify(prods), 200
            return prods, 200
        except Exception as e:
            return {"error": e}, 400
    else:
        import ipdb; ipdb.set_trace()

if __name__ == "__main__":
    app.run(port=5555, debug=True)
