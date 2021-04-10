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



class AdminAddRoleView(BaseView):
    """ Een pagina met een form om AddRole te gebruiken, admin kan hier een role aan een user toevoegen
    """
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        # code voor de form
        form = AddRoleForm()
        if form.validate_on_submit():
            username = form.username.data
            user = User.query.filter_by(username = username).first()
            rolename = form.rolename.data
            role = Role.query.filter_by(name = rolename)
            # check of user en role bestaan in de andere tabellen
            if user == "":
                flash("username niet correct")
            elif role == "":
                flash("Role bestaat niet")
            else:
                addRole(user.id, rolename)
                flash('Gelukt!')

        return self.render('addrole.html', form=form)



    pass

class AdminUserRolesView(AdminModelView):
    """ hier moet een overzicht van users en roles komen (liefst in een tabel)
    """
    pass




admin = Admin(app, index_view=AdminHomeView())

# add views
admin.add_view(AdminModelView(User, db.session)) # werkt voor nu
admin.add_view(AdminModelView(Role, db.session)) # werkt voor nu

admin.add_view(AdminAddRoleView(name="Add Role", url="/addrole"))

admin.add_view(AdminModelView(UserRoles, db.session)) 
admin.add_view(AdminModelView(Language, db.session))
admin.add_view(AdminModelView(Lecture, db.session))

# misschien dat we dit ook zo kunnen maken dat het voor de admin makkelijker is om dingen toe te voegen
# ga ik nog naar kijken