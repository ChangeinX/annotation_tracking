from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
)
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_login import login_user, current_user

from app import db
from .forms import LoginForm
from ..models import User

auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="auth",
)

auth_bp.storage = SQLAlchemyStorage(User, db.session, user=current_user)


@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("annotation_table.annotation_table"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("file_manager.file_manager"))
    return render_template("auth/login.html", title="Sign In", form=form)
