from flask import current_app, flash, redirect, render_template
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
    form_choices = {'role_id': [
        ('1', 'student'), ('2', 'docent'), ('3', 'admin')
    ]}
    column_sortable_list = ('email', 'username', 'role_id')


class AdminRoleView(AdminModelView):
    """ Ook id is te zien zo
    Kunt hier aanpassen welke kolommen te zien zijn
    """
    column_display_pk = True
    column_list = ['id', 'name']
    can_edit = False
    can_create = False
    can_delete = False

class AdminLanguageView(AdminModelView):
    column_display_pk = True
    column_list = ['id', 'language']

class AdminCourseView(AdminModelView):
    column_display_pk = True 
    column_list = ['id', 'teacher_id', 'language_id', 'location', 'cost', 'description']
    can_create = False
    column_sortable_list = ('id', 'teacher_id', 'language_id', 'location')
    form_columns = ('teacher_id', 'language_id', 'location', 'cost', 'description')

class AdminAddCourseView(BaseView):
    """ eigen form die een course toevoegd dmv naam, taal en locatie
    """
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        form = AddCourseForm()

        if form.validate_on_submit():
            username = form.username.data
            language = form.language.data
            location = form.location.data
            cost     = form.cost.data
            description = form.description.data

            # check if some is a teacher
            user = User.query.filter_by(username = username).first()
            language = Language.query.filter_by(language = language).first()
            if user.role_id != 2:
                flash("deze user is geen docent")
            elif language == None:
                flash("deze taal bestaat niet")
            else:
                course = Course(teacher_id = user.id, 
                                language_id = language.id,
                                location = location,
                                cost = cost,
                                description = description)
                db.session.add(course)
                db.session.commit()
                flash("course toegevoegd")
                return self.render("addcourse.html", form=form)

        return self.render("addcourse.html", form=form)


class AdminLectureView(AdminModelView):
    column_display_pk = True 
    # column_hide_backrefs = False
    column_list = ['course_id', 'start_time', 'end_time', 'lecture_name']
    form_columns = ('course_id', 'start_time', 'end_time', 'lecture_name')
    column_sortable_list = ('course_id', 'start_time', 'end_time', 'lecture_name')

    def validate_form(self, form):
        """ Custom validation code that checks dates """
        if form.start_time.data != None and form.end_time.data != None:
            if form.start_time.data >= form.end_time.data:
                flash("Starttijd mag niet later zijn dan de eindtijd")
                return False
        return super(AdminLectureView, self).validate_form(form)


# Ik denk dat dit nu overbodig is
class AdminAddLectureView(BaseView):
    """ eigen form ipv gewone lectureview, kan eventueel nog gemaakt worden
    """
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        form = AddLectureForm()
        if form.validate_on_submit():
            course_id = form.course_id.data
            start_time = form.start_time.data
            end_time = form. end_time.data
            lecture_name = form.lecture_name.data

            if end_time <= start_time:
                flash("Geen geldige eind- en starttijd")
            else:
                lecture = Lecture(course_id = course_id,
                                  start_time = start_time,
                                  end_time = end_time,
                                  lecture_name = lecture_name)
                db.session.add(lecture)
                db.session.commit()
                flash("lecture toegevoegd")
                return self.render("addlecture.html", form=form)                                 

        
        return self.render("addlecture.html", form=form)

class AdminExit(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('index'))


admin = Admin(app, index_view=AdminHomeView())

# add views
admin.add_view(AdminUserView(User, db.session)) # werkt voor nu
admin.add_view(AdminRoleView(Role, db.session)) # werkt voor nu
admin.add_view(AdminLanguageView(Language, db.session)) # werkt voor nu

admin.add_view(AdminCourseView(Course, db.session))
admin.add_view(AdminAddCourseView(name="Add Course", url="/addcourse"))
admin.add_view(AdminLectureView(Lecture, db.session))
# admin.add_view(AdminAddLectureView(name="Add Lecture", url="/addlecture")) # Overbodig, verwijderen?
admin.add_view(AdminExit(name='Exit'))
