from flask import Flask, request, jsonify, make_response, g
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
    return make_response({"error": f"Global: {error.description}"}, 404)

@app.before_request
def preload_production():
    if request.endpoint == "productionbyid":
        id = request.view_args.get("id")
        production = Production.query.get_or_404(
            id, f"I could not find a production with ID {id}"
        )
        g.production = production

class Homepage(Resource):
    def get(self):
        return "Hello World!"

api.add_resource(Homepage, "/")

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
            return {"error": str(e)}, 400

api.add_resource(Productions, "/productions")

class ProductionById(Resource):
    def get(self, id):
        try:
            return make_response(
                    g.production.to_dict(),
                    200,
                )
        except Exception as e:
            return make_response({"error": str(e)}, 400)

    def patch(self, id):
        try:
            data = request.json
            for k, v in data.items(): #! Mass Assignment
                if hasattr(g.production, k):
                    setattr(g.production, k, v) #! HERE model validations will kick in!
            db.session.commit()
            return make_response(g.production.to_dict(), 202)
        except Exception as e:
            return {"error": str(e)}, 400

    def delete(self, id):
        try:
            db.session.delete(g.production)
            db.session.commit()
            return make_response("", 204)
        except Exception as e:
            return {"error": str(e)}, 400

api.add_resource(ProductionById, "/productions/<int:id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
