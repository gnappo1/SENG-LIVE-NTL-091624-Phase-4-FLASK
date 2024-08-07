#!/usr/bin/env python3

#! 📚 Review With Students:
# API Fundamentals
# MVC Architecture and Patterns / Best Practices
# RESTful Routing
# Serialization
# Postman

#! Set Up When starting from scratch:
# In Terminal, `cd` into `server` and run the following:
# export FLASK_APP=app.py
# export FLASK_RUN_PORT=5555
# flask db init
# flask db migrate -m 'Create tables'
# flask db upgrade
# python seed.py


from flask import Flask, request, jsonify, make_response, render_template, g
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Production, CrewMember
from werkzeug.exceptions import NotFound
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///theater.db"

#! Ideal configuration for all your apps
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#! Set up the connection between app and db for alembic - MIGRATION VERSION CONTROL
migrate = Migrate(app, db)
#! Set up the connection between app and db for SQLAlchemy
db.init_app(app)
#! Set up Flask-Restful's Api
api = Api(app, prefix="/api/v1")

@app.route("/")
def homepage():
    productions = Production.query.all()
    return render_template("homepage.html", prods=productions)

@app.errorhandler(NotFound)
def page_not_found(error):
    return "This page does not exist", 404

@app.before_request
def load_production():
    if request.endpoint == "productionbyid":
        string_id = request.path.split("/")[-1]
        if prod := Production.query.get(int(string_id)):
            g.production = prod
        else:
            return {"error": f"Could not find a Production with id #{string_id}"}, 404


class Productions(Resource):
    def get(self):
        try:
            serialized_prods = [prod.to_dict() for prod in Production.query]
            return make_response(serialized_prods, 200)
            # return serialized_prods, 200
        except Exception as e:
            return {"error": str(e)}
    
    def post(self):
        try:
            data = request.get_json() #! you might get a 405 if content type has not been set
            prod = Production(**data) #! model validations kick in at this point
            db.session.add(prod)
            db.session.commit() #! database constraints kick in
            return prod.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400

class ProductionByID(Resource):
    def get(self, id):
        try:
            return g.production.to_dict(rules=("crew_members",)), 200
        except Exception as e:
            return {"error": str(e)}, 400

    def patch(self, id):
        try:
            #! extract request's data
            data = request.get_json()
            #! use the data to patch the object
            for attr, value in data.items():
                setattr(g.production, attr, value) #! MODEL VALIDATIONS KICK IN HERE
            db.session.commit()
            #! return the serialized patched object
            return g.production.to_dict(rules=("crew_members",)), 202
        except Exception as e:
            return {"error": str(e)}, 422

    def delete(self, id):
        try:
            db.session.delete(g.production)
            db.session.commit()
            return {}, 204
        except Exception as e:
            return {"error": str(e)}, 422

api.add_resource(Productions, "/productions")
api.add_resource(ProductionByID, "/productions/<int:id>")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
