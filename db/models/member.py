from db.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    accounts = relationship("Account", back_populates="member")
    transactions = relationship("CC050", back_populates="clearing_member_")
    eod_transactions = relationship("CI050", back_populates="clearing_member_")
    issues = relationship("Issue", back_populates="bank")
