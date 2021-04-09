from flask import render_template, flash, redirect, url_for, current_app
from flask_login import current_user
from project.forms import *
from project.models import *
from flask_sqlalchemy import SQLAlchemy
from project import app
from functools import wraps

# weet niet waar dit moet, dus dit mag verplaatst worden :)
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
            if urole != role:
                return current_app.login_manager.unauthorized()
            return func(*args, **kwargs)
        return decorated_view
    return wrapper

    
def addRole(uid, rolename):
    """ adds a role to user, in UserRoles table"""
    user = User.query.filter_by(id=uid).first()
    role = Role.query.filter_by(name = rolename).first()
    userrole = UserRoles(user_id = user.id, role_id = role.id)
    db.session.add(userrole)
    db.session.commit()


def getRole(uid):
    """ gets role name """
    user = UserRoles.query.filter_by(user_id=uid).first()
    role = Role.query.filter_by(id = user.role_id).first()
    return role.name