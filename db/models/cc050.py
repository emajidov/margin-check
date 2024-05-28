from db.base import Base
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship


class CC050(Base):
    __tablename__ = 'cc050'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    clearing_member = Column(ForeignKey("members.id"))
    account = Column(ForeignKey("accounts.id"))
    margin_type = Column(String)
    margin = Column(Float)

    clearing_member_ = relationship("Member", back_populates="transactions")
    account_ = relationship("Account", back_populates="transactions")
    issue = relationship("Issue", back_populates="cc050")