from flask import Flask, request, jsonify
from flask_migrate import Migrate

from models import db, Production, CrewMember

app = Flask(__name__)
#! set up some configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///theater.db" #! required
app.config["SQLALCHEMY_ECHO"] = True #* ideal!
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #* ideal!

#! connect to the models and migrations
#! connection between app and alembic
migrate = Migrate(app, db)

#! connection between app and sqlalchemy
db.init_app(app)

@app.route("/")
def homepage():
    return "Hello World!"


@app.route("/productions", methods=["GET", "POST"])
def productions():
    if request.method == "GET":
        try:
            prods = [production.as_dict() for production in Production.query.all()]
            return prods, 200
            # return jsonify(prods), 200
            # return make_response(prods, 200)
        except Exception as e:
            return {"error": str(e)}, 400
    else:
        try:
            #! extract the data out of the request body
            data = request.json
            #! Instantiate an object
            new_production = Production(**data) #! here model validations (properties or @validates properties) will kick in
            #! Make sure the ... is tracking it
            db.session.add(new_production) #! no particular validations kick in here!
            #! Make sure you commit!!!
            db.session.commit() #! Here is when db constraints will kick in!
            return new_production.as_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)
