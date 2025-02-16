from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, relationship
from dataclasses import dataclass

# sqlalchemy constructor
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

@dataclass
class Make(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    createdOn: Mapped[datetime]
    updatedOn: Mapped[datetime]

@dataclass
class Model(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    createdOn: Mapped[datetime]
    updatedOn: Mapped[datetime]

@dataclass
class MakeModel(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    makeId: Mapped[int] = mapped_column(ForeignKey("make.id"))
    modelId: Mapped[datetime] = mapped_column(ForeignKey("model.id"))
    createdOn: Mapped[datetime]
    updatedOn: Mapped[datetime]

    make: Mapped[Make] = relationship()
    model: Mapped[Model] = relationship()