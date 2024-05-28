from db.base import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    bank_id = Column(Integer, ForeignKey('members.id'))

    member = relationship("Member", back_populates="accounts")
    transactions = relationship("CC050", back_populates="account_")
    eod_transactions = relationship("CI050", back_populates="account_")
    issues = relationship("Issue", back_populates="account")