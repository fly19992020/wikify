import os
from urllib.parse import unquote

import flask
import markupsafe
from flask import Blueprint, request, redirect, abort, send_from_directory, g, render_template

from .history_base import history_base
from .page_base import page_base
from .user_base import user_base, priv_base

routes = Blueprint("routes", __name__)

from .wikiserver import setting

@routes.route("/R/<path:page_name>")
def raw(page_name: str):
    return send_from_directory(os.getcwd() + "/" + setting.prefix, page_name)

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

    html = base.get_page(page_name, g.get("username"))
    return html, 200, {"Content-Type": "text/html; charset=utf-8"}


@routes.route("/Spec/<path:page_name>")
def special_page(page_name: str):
    if page_name == "Search":
        pb = page_base.PageBase(setting.database, setting.prefix)
        rs = pb.search_for(request.args.get("search"))
        g.page = "<p>Searching for {}.</p>".format(request.args.get("search"))
        for i in rs:
            g.page += "<a href=\"/{}\">{}</a>".format(i[0], i[0])
            g.page += "<br>"
            print("page")
        if not g.get("page"):
            g.page += "<p>No matched results. </p>"
    if g.get("page"):
        return render_template("country.html",
                               Title="Wikify",
                               Home=markupsafe.Markup("<a href=\"/\">Home</a>"),
                               Body=markupsafe.Markup(g.page),
                               Source=False,
                               Username=g.get("username"),
                               Views={}
                               )
    abort(500)


@routes.route("/<path:page_name>", methods=["PUT"])
def save_page(page_name: str):
    base = page_base.PageBase(setting.database, setting.prefix)
    page_name = unquote(page_name)

    if not request.data:
        abort(400)

    pvb = priv_base.PrivBase(setting.database)
    if not pvb.check_edit(g.get("username")):
        abort(403)

    base.write_page(page_name, request.data.decode("utf-8"))

    hb = history_base.HistoryBase(setting.database)
    hb.add_history(g.get("username"), page_name)
    return "", 200
