from flask import Blueprint, redirect, url_for
from flask_login import login_required

general_bp = Blueprint(
    "general",
    __name__,
    static_url_path="general",
    static_folder="static",
    template_folder="templates",
)


@general_bp.route("/")
@login_required
def home():
    return redirect(url_for("table.annotation_table"))
