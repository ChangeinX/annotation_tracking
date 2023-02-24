from flask import Blueprint, render_template
from flask_login import login_required

table_bp = Blueprint("table", __name__, static_url_path="api", template_folder="templates")


@table_bp.route("/")
@login_required
def table():
    return render_template("annotation_table/annotation_table.html")
