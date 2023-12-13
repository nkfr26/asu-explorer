from flask_admin.contrib.sqla import ModelView
from flask import Response, redirect
from werkzeug.exceptions import HTTPException

class AuthModelView(ModelView):
    column_display_pk = True

    def __init__(self, model, session, basic_auth):
        super().__init__(model, session)
        self.basic_auth = basic_auth

    def is_accessible(self):
        if not self.basic_auth.authenticate():
            raise HTTPException(response=Response(
                response="""
                    <h1>Unauthorized</h1>
                    <p>You could not be authenticated. Please refresh the page.</p>
                """, status=401, headers={"WWW-Authenticate": "Basic"}
            ))

        return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(self.basic_auth.challenge())