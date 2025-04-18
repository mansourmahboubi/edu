"""empty message

Revision ID: c35882901ea6
Revises: 95846b0d7ef4
Create Date: 2022-12-04 19:52:42.750186

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c35882901ea6"
down_revision = "95846b0d7ef4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("is_superuser", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_users_email"),
        "users",
        ["email"],
        unique=True,
    )
    op.create_index(
        op.f("ix_users_full_name"),
        "users",
        ["full_name"],
        unique=False,
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.drop_index("ix_user_email", table_name="user")
    op.drop_index("ix_user_full_name", table_name="user")
    op.drop_index("ix_user_id", table_name="user")
    op.drop_table("user")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column(
            "id",
            sa.INTEGER(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "full_name",
            sa.VARCHAR(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "email",
            sa.VARCHAR(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "hashed_password",
            sa.VARCHAR(),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.BOOLEAN(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "is_superuser",
            sa.BOOLEAN(),
            autoincrement=False,
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id", name="user_pkey"),
    )
    op.create_index("ix_user_id", "user", ["id"], unique=False)
    op.create_index(
        "ix_user_full_name",
        "user",
        ["full_name"],
        unique=False,
    )
    op.create_index("ix_user_email", "user", ["email"], unique=False)
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_full_name"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
