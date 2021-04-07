from flask import render_template
from flask.blueprints import Blueprint
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from project.models import *
from project import app

# /admin


admin_blueprint = Blueprint('administrator',
                             __name__,
                             template_folder='templates/admin')

class AdminModelView(ModelView):
    def is_accessible(self):
        if getRole(current_user.id) == "admin":
            return True
        return False

admin = Admin(app)
admin.add_view(AdminModelView(User, db.session))