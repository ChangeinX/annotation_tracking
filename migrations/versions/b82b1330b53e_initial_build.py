"""Initial build

Revision ID: b82b1330b53e
Revises: 
Create Date: 2023-02-23 10:34:16.807423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b82b1330b53e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=True),
        sa.Column("default", sa.Boolean(), nullable=True),
        sa.Column("permissions", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    with op.batch_alter_table("roles", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_roles_default"), ["default"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=True),
        sa.Column("first_name", sa.String(length=64), nullable=True),
        sa.Column("last_name", sa.String(length=64), nullable=True),
        sa.Column("email", sa.String(length=64), nullable=True),
        sa.Column("password_hash", sa.String(length=128), nullable=True),
        sa.Column("role_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_users_email"), ["email"], unique=True)
        batch_op.create_index(
            batch_op.f("ix_users_username"), ["username"], unique=True
        )

    op.create_table(
        "annotation_tracking",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("site_id", sa.String(length=64), nullable=True),
        sa.Column("donation_id", sa.String(length=64), nullable=True),
        sa.Column("video_id", sa.String(length=64), nullable=True),
        sa.Column("segment_id", sa.String(length=64), nullable=True),
        sa.Column("stage", sa.String(length=64), nullable=True),
        sa.Column("video_length", sa.String(length=64), nullable=True),
        sa.Column("assigned_on", sa.DateTime(), nullable=True),
        sa.Column("assigned_to", sa.String(length=64), nullable=True),
        sa.Column("completed_on", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("annotation_tracking")
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_users_username"))
        batch_op.drop_index(batch_op.f("ix_users_email"))

    op.drop_table("users")
    with op.batch_alter_table("roles", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_roles_default"))

    op.drop_table("roles")
    # ### end Alembic commands ###
