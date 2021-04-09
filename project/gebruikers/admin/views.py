from flask import render_template, flash, redirect, url_for
from flask.blueprints import Blueprint
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required
from project.models import *
from project import app
from project.roles import *

# /admin

admin_blueprint = Blueprint('administrator',
                             __name__,
                             template_folder='templates/admin')


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if getRole(current_user.id) == "admin":
                return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('standaard.login'))

class AdminModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            if getRole(current_user.id) == "admin":
                return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('standaard.login'))


#views
admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Role, db.session))
admin.add_view(AdminModelView(UserRoles, db.session))
admin.add_view(AdminModelView(Language, db.session))
admin.add_view(AdminModelView(Lecture, db.session))

# misschien dat we dit ook zo kunnen maken dat het voor de admin makkelijker is om dingen toe te voegen
# ga ik nog naar kijken