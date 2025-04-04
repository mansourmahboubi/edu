from fastapi_third.db.base import Base
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String


class DummyModel(Base):
    """Model for demo purpose."""

    __tablename__ = "dummy_model"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(length=200))  # noqa: WPS432
