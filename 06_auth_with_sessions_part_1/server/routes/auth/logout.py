from routes.__init__ import Resource, make_response, session

class Logout(Resource):
    def delete(self):
        try:
            response = make_response({}, 204)
            #! 1. if no one is logged in, there is no one to logout
            #! 2. but if we do, then we need to remove their traces from the session
            if "user_id" in session:
                del session["user_id"]
            response.delete_cookie("session")
            return response
        except Exception as e:
            return {"error": str(e)}, 422
