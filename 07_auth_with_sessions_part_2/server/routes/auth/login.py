from routes.__init__ import Resource, request, db, make_response, session
from models.user import User

class Login(Resource):
    def post(self):
        try:
            #! 1. Get the data through the request context
            data = request.json
            #! Check that you can find a user by that email AND that the password matches
            user = User.query.filter_by(email=data.get("email", "")).first()
            if user and user.authenticate(data.get("password", "")):
                #! if so, you can login the user (aka store their id in the session)
                session["user_id"] = user.id #! THIS IS HOW WE LOGIN
                return make_response(user.to_dict(), 200)
            else:
                return make_response("Invalid Credentials", 401)
        except Exception as e:
            return {"error": str(e)}, 400
