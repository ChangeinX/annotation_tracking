from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

import config
from app import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == config.Config.ADMIN:
                self.role = Role.query.filter_by(name="Administrator").first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTRATOR)

    def __repr__(self):
        return f"{self.username}"


class Permission:
    VIEW_TABLE = 0x01
    EDIT_TABLE = 0x02
    ADMINISTRATOR = 0x80


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            "Viewer": (Permission.VIEW_TABLE, True),
            "Editor": (Permission.VIEW_TABLE | Permission.EDIT_TABLE, False),
            "Administrator": (0xFF, False),
        }
        default_role = "Viewer"

        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return f"{self.name}"


class AnnotationTracking(db.Model):
    __tablename__ = "annotation_tracking"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    site_id = db.Column(db.String(64))
    video_id = db.Column(db.String(64))
    segment_id = db.Column(db.String(64))
    stage = db.Column(db.String(64))
    video_length = db.Column(db.String(64))
    expected_completion_time = db.Column(db.String(64))
    actual_completion_time = db.Column(db.String(64))
    assigned_to = db.Column(db.String(64))

    def to_dict(self):
        return {
            "site_id": self.site_id,
            "video_id": self.video_id,
            "segment_id": self.segment_id,
            "stage": self.stage,
            "video_length": self.video_length,
            "expected_completion_time": self.expected_completion_time,
            "actual_completion_time": self.actual_completion_time,
            "assigned_to": self.assigned_to
        }

    def __repr__(self):
        return f"{self.site_id} - {self.video_id} - {self.segment_id} - {self.stage}"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_all():
    db.create_all()
    Role.insert_roles()
