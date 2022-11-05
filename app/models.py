from typing import Optional, Dict, Union

import ormar
import databases
import sqlalchemy
import datetime

from .config import settings

metadata = sqlalchemy.MetaData()
database = databases.Database(settings.db_url)


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Category(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = "category"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=248, unique=True, nullable=False)


class Notes(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = "notes"

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=248, nullable=False)
    body: str = ormar.String(max_length=1248, nullable=False)
    category: Optional[Union[Category, Dict]] = ormar.ForeignKey(Category)
    timestamp: datetime.datetime = ormar.DateTime(
        pydantic_only=True, default=datetime.datetime.now
    )


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
