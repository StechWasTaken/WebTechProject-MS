from flask import render_template, flash, redirect, url_for, current_app
from flask_login import current_user
from project.forms import *
from project.models import *
from flask_sqlalchemy import SQLAlchemy, event
from project import app
from functools import wraps

# Dit is de plek waar alle role gerelateerde code staat


def role_required(role="ANY"):
    """maakt een wrapper waar de role gecheckt wordt
    als de current_user niet de juiste role heeft krijgt hij een unauthorized pagina te zien
    """
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            urole = ""
            if current_user.is_authenticated:
                urole = getRole(current_user.id)
            if role not in urole:
                return current_app.login_manager.unauthorized()
            return func(*args, **kwargs)
        return decorated_view
    return wrapper

    
def addRole(uid, rolename):
    """ adds a role to user, in UserRoles table"""
    user = User.query.filter_by(id=uid).first()
    role = Role.query.filter_by(name = rolename).first()
    # check if user exists in UserRoles, zo niet voeg toe
    if UserRoles.query.filter_by(user_id = user.id) == "":
        userrole = UserRoles(user_id = user.id, role_id = role.id)
        db.session.add(userrole)
    # zo wel, append de role met de bestaande roles en voeg toe
    else:
        existing_user = UserRoles.query.filter_by(user_id = user.id)
        existing_roles = user.role_id
        existing_roles.append(role.id)
        existing_user.role_id = existing_roles
        db.session.add(existing_user)

    db.session.commit()


def getRole(uid):
    """ gets role name """
    user = UserRoles.query.filter_by(user_id=uid).first()
    role = Role.query.filter_by(id = user.role_id).first()
    return role.name

# in het geval dat een user wordt aangemaakt wordt de student role automatisch toegevoegd
@event.listens_for(User.id, 'set', retval=True)
def addStudentRole():
    addRole(User.id, 'student')
    return