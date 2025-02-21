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

@dataclass
class Suggestions(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    phoneNumber: Mapped[str]
    email: Mapped[str]
    suggestion: Mapped[str]

# Manual Class for Vin Decode Procedure Result
@dataclass
class VinResult:
    attributeId: str = ""
    code: str = ""
    createdOn: datetime = None
    dataType: str = ""
    decode: str = ""
    elementId: int = None
    groupName: str = ""
    keys: str = ""
    patternId: int = None
    source: str = ""
    value: str = ""
    variable: str = ""
    vinSchemaId: int = None
    wmiId: int = None