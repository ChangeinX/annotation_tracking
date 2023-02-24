from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
)
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_login import login_user, logout_user, current_user

from app import db
from .forms import LoginForm, RegistrationForm
from ..models import User

auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="auth",
)

auth_bp.storage = SQLAlchemyStorage(User, db.session, user=current_user)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("table.annotation_table"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("table.annotation_table"))
    return render_template("auth/login.html", title="Sign In", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("general.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        login_user(user)
        return redirect(url_for("table.annotation_table"))
    return render_template("auth/register.html", title="Register", form=form)


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
