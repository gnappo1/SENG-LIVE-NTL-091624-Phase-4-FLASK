#!/usr/bin/env python3

#! Set Up When starting from scratch:
# In Terminal, `cd` into `server` and run the following:
# export FLASK_APP=app.py
# export FLASK_RUN_PORT=5555
# flask db init
# flask db migrate -m 'Create tables'
# flask db upgrade
# python seed.py

#! External libraries imports
from flask import request, g, render_template, session
from werkzeug.exceptions import NotFound

#! Internal imports
from app_config import app, api, db
from models.production import Production
from models.crew_member import CrewMember
from models.user import User
from routes.crew_member.crew_member_by_id import CrewMemberByID
from routes.crew_member.crew_members import CrewMembers
from routes.production.production_by_id import ProductionByID
from routes.production.productions import Productions
from routes.auth.login import Login
from routes.auth.signup import Signup
from routes.auth.logout import Logout
from routes.auth.current_user import CurrentUser

#! ==================
#! GENERAL ROUTE CONCERNS

@app.errorhandler(NotFound)
def not_found(error):
    return {"error": error.description}, 404


@app.before_request
def before_request():
    #! First refactor when inserting crew routes BUT not very DRY right?
    # if request.endpoint == "productionbyid":
    #     id = request.view_args.get("id")
    #     prod = db.session.get(Production, id)
    #     g.prod = prod
    # elif request.endpoint == "crewmemberbyid":
    #     id = request.view_args.get("id")
    #     crew = db.session.get(CrewMember, id)
    #     g.crew = crew
    #! Better Approach
    path_dict = {"productionbyid": Production, "crewmemberbyid": CrewMember}
    if request.endpoint in path_dict:
        id = request.view_args.get("id")
        if record := db.session.get(path_dict.get(request.endpoint), id):
            key_name = "production" if request.endpoint == "productionbyid" else "crew"
            setattr(g, key_name, record)
        else:
            return {
                "error": f"Could not find a {path_dict.get(request.endpoint).__name__} with id #{id}"
            }, 404


#!======================
#! API ROUTES


@app.route("/")
def homepage():
    productions = Production.query.order_by("title")
    crew_members = CrewMember.query.order_by("name")
    return render_template(
        "homepage.html", prods=productions, crew_members=crew_members
    )


api.add_resource(Productions, "/productions")
api.add_resource(ProductionByID, "/productions/<int:id>")
api.add_resource(CrewMembers, "/crew-members")
api.add_resource(CrewMemberByID, "/crew-members/<int:id>")
api.add_resource(Signup, "/signup")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")
api.add_resource(CurrentUser, "/current-user")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
