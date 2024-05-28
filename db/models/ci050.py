from db.base import Base
from sqlalchemy import Column, Date, DateTime, String, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship


class CI050(Base):
    __tablename__ = 'ci050'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    time_of_day = Column(DateTime)
    clearing_member = Column(ForeignKey("members.id"))
    account = Column(ForeignKey("accounts.id"))
    margin_type = Column(String)
    margin = Column(Float)

    clearing_member_ = relationship("Member", back_populates="eod_transactions")
    account_ = relationship("Account", back_populates="eod_transactions")
    issue = relationship("Issue", back_populates="ci050")
