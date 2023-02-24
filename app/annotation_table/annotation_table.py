from flask import Blueprint, render_template, make_response
from flask_wtf.csrf import generate_csrf
from flask_login import login_required

table_bp = Blueprint(
    "table", __name__, static_url_path="table", template_folder="templates", static_folder="static"
)


@table_bp.route("/")
@login_required
def annotation_table():
    csrf_token = generate_csrf()
    response = make_response(render_template("annotation_table/annotation_table.html"))
    response.set_cookie("csrf_token", csrf_token)
    return response
