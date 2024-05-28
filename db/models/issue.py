from db.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime


class Issue(Base):
    __tablename__ = 'issues'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    bank_id = Column(ForeignKey("members.id"))
    account_id = Column(ForeignKey("accounts.id"))
    created_at = Column(DateTime, default=datetime.now())
    previous_margin = Column(Float)
    current_margin = Column(Float)
    ci050_id = Column(Integer, ForeignKey("ci050.id"))
    cc050_id = Column(Integer, ForeignKey("cc050.id"))

    bank = relationship("Member", back_populates="issues")
    account = relationship("Account", back_populates="issues")
    cc050 = relationship("CC050", back_populates="issue")
    ci050 = relationship("CI050", back_populates="issue")