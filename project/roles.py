from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from project.forms import *
from project.models import *
from project import app
from functools import wraps

# weet niet waar dit moet, dus dit mag verplaatst worden :)
# dit werkt nog niet
def role_required(role="ANY"):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            urole = ""
            if current_user.is_authenticated:
                urole = getRole(current_user.id)
            if urole != role:
                return current_app.login_manager.unauthorized()
        return decorated_view
    return wrapper