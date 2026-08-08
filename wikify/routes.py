import os
from urllib.parse import unquote

import flask
import markupsafe
from flask import Blueprint, request, redirect, abort, send_from_directory, g

from .history_base import history_base
from .page_base import page_base
from .user_base import user_base

routes = Blueprint("routes", __name__)

from .wikiserver import setting

@routes.route("/editor.js")
def editor_js():
    return send_from_directory(os.getcwd() + "/" + setting.prefix, "editor.js")


@routes.route("/editor.html")
def editor_html():
    return send_from_directory(os.getcwd() + "/" + setting.prefix, "editor.html")


@routes.route("/login.js")
def login_js():
    return send_from_directory(os.getcwd() + setting.prefix, "login.js")


@routes.route("/login.html")
def login_html():
    return send_from_directory(os.getcwd() + setting.prefix, "login.html")


@routes.route("/login.html", methods=["POST"])
def login():
    data = request.get_json()
    ub = user_base.UserBase(setting.database)
    if ub.check_password(data["name"], data["password"]):
        r = flask.make_response()
        r.set_cookie("name", data["name"])
        r.set_cookie("password", data["password"])
        r.status_code = 200
        r.set_data("")
        return r
    else:
        abort(401)


@routes.route("/")
def root():
    return redirect("/index.html")


@routes.route("/index.html")
def index():
    return redirect("/Home")


@routes.route("/favicon.ico")
def favicon():
    abort(404)


@routes.route("/<path:page_name>")
def page(page_name: str):
    base = page_base.PageBase(setting.database, setting.prefix)
    page_name = unquote(page_name)

    # ?source=true
    if request.args.get("source") == "true":
        content = base.get_source(page_name)
        return content, 200, {"Content-Type": "text/plain; charset=utf-8"}

    html = base.get_page(page_name)
    return html, 200, {"Content-Type": "text/html; charset=utf-8"}


@routes.route("/<path:page_name>", methods=["PUT"])
def save_page(page_name: str):
    base = page_base.PageBase(setting.database, setting.prefix)
    page_name = unquote(page_name)

    if not request.data:
        abort(400)

    base.write_page(page_name, request.data.decode("utf-8"))

    hb = history_base.HistoryBase(setting.database)
    hb.add_history(g.get("username"), page_name)
    return "", 200
