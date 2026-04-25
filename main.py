# SPDX-License-Identifier: AGPL-3.0-only
import os
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import declarative_base, Session

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL, future=True)
Base = declarative_base()


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


Base.metadata.create_all(engine)
with Session(engine) as _s:
    if _s.scalar(select(Item).limit(1)) is None:
        _s.add_all([Item(name="alpha"), Item(name="beta")])
        _s.commit()

app = FastAPI(title="ploydok fixture-fastapi")

BUILD_ID = os.environ.get("PLOYDOK_BUILD_ID", "unknown")


def _list_items():
    with Session(engine) as s:
        rows = s.scalars(select(Item).order_by(Item.id)).all()
        return [{"id": r.id, "name": r.name} for r in rows]


@app.get("/")
def root():
    return {"build": BUILD_ID, "items": _list_items()}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items")
def items():
    return _list_items()
