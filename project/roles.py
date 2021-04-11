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
    admins mogen alles zien mhahaha
    """
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            urole = ""
            if current_user.is_authenticated:
                urole = getRole(current_user.id)
            if role != urole or role != 'admin':
                return current_app.login_manager.unauthorized()
            return func(*args, **kwargs)
        return decorated_view
    return wrapper


# Dit is nu enigssinds overbodig, maar in principe nog wel bruikbaar
def addRole(uid, rolename):
    """ adds a role to user"""
    user = User.query.filter_by(id=uid).first()
    role = Role.query.filter_by(name = rolename).first()
    user.role_id = role.id
    db.session.add(user)
    db.session.commit()


def getRole(uid):
    """ gets role name """
    user = User.query.filter_by(id=uid).first()
    role = Role.query.filter_by(id = user.role_id).first()
    return role.name
