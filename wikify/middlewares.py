from flask import Blueprint, request, g, abort

from wikify.user_base.user_base import UserBase
from .wikiserver import setting

middlewares = Blueprint("middlewares", __name__)

@middlewares.before_app_request
def auth():
    user = request.cookies.get("name", "Guest")
    if user == "Guest":
        g.username = user
        return
    ub = UserBase(setting.database)
    if ub.check_password(user, request.cookies.get("password", "")):
        g.username = user
        return
    print(user)
    abort(401)
