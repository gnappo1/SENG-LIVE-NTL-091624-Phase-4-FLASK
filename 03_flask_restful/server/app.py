from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

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

#! set up the flask-restful API
api = Api(app, prefix="/api/v1")

@app.errorhandler(404)
def page_not_found(error):
    return make_response({"error": error.description}, 404)


@app.route("/")
def homepage():
    return "Hello World!"

class Productions(Resource):
    def get(self):
        try:
            serialized_prods = [
                production.to_dict(rules=("-crew_members",)) for production in Production.query
            ]
            return make_response(serialized_prods, 200)
        except Exception as e:
            return make_response({"error": str(e)}, 400)

    def post(self):
        try:
            #! extract the data out of the request body
            data = request.json
            #! Instantiate an object
            new_production = Production(**data) #! here model validations (properties or @validates properties) will kick in
            #! Make sure the ... is tracking it
            db.session.add(new_production) #! no particular validations kick in here!
            #! Make sure you commit!!!
            db.session.commit() #! Here is when db constraints will kick in!
            return new_production.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400

api.add_resource(Productions, "/productions")

class ProductionById(Resource):
    def get(self, id):
        try:
            #! retrieve the production with the id provided (if existing)
            # production = db.session.get(Production, id) #! returns nothing if no records are found -> None
            if production := db.session.get(Production, id):
                return make_response(
                    production.to_dict(),
                    200,
                )
            else:
                return make_response({"error": f"Could not find a production with id {id}"}, 404)
        except Exception as e:
            return make_response({"error": str(e)}, 400)

api.add_resource(ProductionById, "/productions/<int:id>")
# @app.route("/productions", methods=["GET", "POST"])
# def productions():
#     if request.method == "GET":
#         try:
#             prods = [production.as_dict() for production in Production.query.all()]
#             return prods, 200
#             # return jsonify(prods), 200
#             # return make_response(prods, 200)
#         except Exception as e:
#             return {"error": str(e)}, 400
#     else:
#         try:
#             #! extract the data out of the request body
#             data = request.json
#             #! Instantiate an object
#             new_production = Production(**data) #! here model validations (properties or @validates properties) will kick in
#             #! Make sure the ... is tracking it
#             db.session.add(new_production) #! no particular validations kick in here!
#             #! Make sure you commit!!!
#             db.session.commit() #! Here is when db constraints will kick in!
#             return new_production.as_dict(), 201
#         except Exception as e:
#             db.session.rollback()
#             return {"error": str(e)}, 400


if __name__ == "__main__":
    app.run(port=5555, debug=True)
