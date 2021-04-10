from flask import render_template, flash, redirect, url_for, current_app
from flask.blueprints import Blueprint
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_required
from project.models import *
from project import app
from project.roles import *

# /admin

admin_blueprint = Blueprint('administrator', __name__, template_folder='templates/admin')


class AdminHomeView(AdminIndexView):
    """ Dit is de view voor de admin homepage /admin, index.html """

    @expose('/')
    def index(self):
        name = current_user.username # dit werkt omdat alleen admins hierbij kunnen :)
        return self.render('index.html', username = name)

    def is_accessible(self):
        if current_user.is_authenticated:
            if getRole(current_user.id) == "admin":
                return True

    def inaccessible_callback(self, name, **kwargs):
        return current_app.login_manager.unauthorized()


class AdminModelView(ModelView):
    """ Eigen modelview die checkt op admin role, zodat alleen admins erbij kunnen"""
    def is_accessible(self):
        if current_user.is_authenticated:
            if getRole(current_user.id) == "admin":
                return True

    def inaccessible_callback(self, name, **kwargs):
        return current_app.login_manager.unauthorized()



class AdminAddRoleView(AdminModelView):
    """ hoe doe je dit xD AdminModelView? Iets anders?
    Een view maken naar een pagina met een form om AddRole te gebruiken
    """
    pass





admin = Admin(app, index_view=AdminHomeView())

# add views
admin.add_view(AdminModelView(User, db.session)) # werkt voor nu
admin.add_view(AdminModelView(Role, db.session))
admin.add_view(AdminModelView(UserRoles, db.session))
admin.add_view(AdminModelView(Language, db.session))
admin.add_view(AdminModelView(Lecture, db.session))

# misschien dat we dit ook zo kunnen maken dat het voor de admin makkelijker is om dingen toe te voegen
# ga ik nog naar kijken