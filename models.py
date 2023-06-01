from sqlalchemy import Boolean, Column, Integer, String, Numeric, Date
from database import Base

class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=False, index=True)
    current_price = Column(Numeric(10, 2))
    exp_date = Column(Date)
    strike = Column(Numeric(10, 2))
    type = Column(String)
    premium = Column(Numeric(10, 2))
    open_interest = Column(Integer)
    implied_volatility = Column(Numeric(10, 2))

