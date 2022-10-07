import enum

import pandas as pd
from sqlalchemy import Boolean, CheckConstraint, Column, Integer, String
from sqlalchemy.orm import relationship

from req_enums import City
from sql_global import Base, Engine, Enum, Session


class Hotel(Base):
    __tablename__ = "hotel"
    __table_args__ = (CheckConstraint("0 <= children_policy AND children_policy <= 2"),)
    id = Column("id", Integer, primary_key=True, autoincrement=False)
    group = Column("group", String(64))
    brand = Column("brand", String(64))
    city = Column("city", Enum(City))
    parking = Column("parking", Boolean)
    pool = Column("pool", Boolean)
    children_policy = Column("children_policy", Integer)
    responses = relationship("Response", back_populates="hotel")

    def __repr__(self):
        return f"<Hotel(id={self.id}, group={self.group}, brand={self.brand}, city={self.city}, parking={self.parking}, pool={self.pool}, children_policy={self.children_policy.name})>"

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.c}

    @classmethod
    def list(cls):
        with Session() as session:
            return session.query(cls).all()

    @classmethod
    def update(cls):
        df = pd.read_csv("dataset/features_hotels.csv").rename(
            columns={"hotel_id": "id"}
        )
        df.to_sql(cls.__tablename__, Engine, if_exists="append", index=False)
