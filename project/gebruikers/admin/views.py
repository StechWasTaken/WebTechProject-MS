from flask import current_app, flash
from flask.blueprints import Blueprint
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from project.models import *
from project import app
from project.roles import *
from project.gebruikers.admin.forms import *

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



class AdminUserView(AdminModelView):
    """ ook role_id is te zien zo
    Kunt hier aanpassen welke kolommen te zien zijn
    """
    column_display_pk = True 
    # column_hide_backrefs = False
    column_list = ['email', 'username', 'role_id']
    form_columns = ('email', 'username', 'password', 'role_id')


class AdminRoleView(AdminModelView):
    """ Ook id is te zien zo
    Kunt hier aanpassen welke kolommen te zien zijn
    """
    column_display_pk = True
    # column_hide_backrefs = False
    column_list = ['id', 'name']
    can_edit = False
    can_create = False
    can_delete = False

class AdminLanguageView(AdminModelView):
    pass

class AdminCourseView(AdminModelView):
    pass


class AdminLectureView(AdminModelView):
    pass


admin = Admin(app, index_view=AdminHomeView())

# add views
admin.add_view(AdminUserView(User, db.session)) # werkt voor nu
admin.add_view(AdminRoleView(Role, db.session)) # werkt voor nu

admin.add_view(AdminLanguageView(Language, db.session))
admin.add_view(AdminCourseView(Course, db.session))
admin.add_view(AdminLectureView(Lecture, db.session))


# misschien dat we dit ook zo kunnen maken dat het voor de admin makkelijker is om dingen toe te voegen
# ga ik nog naar kijken