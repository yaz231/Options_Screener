from sqlalchemy import Boolean, Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    symbol = Column(String, unique=False, index=True)
    current_price = Column(Numeric(10, 2))
    exp_date = Column(Date)
    strike = Column(Numeric(10, 2))
    type = Column(String)
    premium = Column(Numeric(10, 2))
    open_interest = Column(Integer)
    implied_volatility = Column(Numeric(10, 2))
    strategy_id = Column(Integer, ForeignKey("option_strategies.id"))
    strategy = relationship("OptionStrategy", back_populates="legs")

    # Additional fields for multi-leg options
    leg_type = Column(String)  # Put/Call
    leg_strike = Column(Numeric(10, 2))
    leg_quantity = Column(Integer)


class OptionStrategy(Base):
    __tablename__ = "option_strategies"

    id = Column(Integer, primary_key=True, index=True)
    strategy_name = Column(String, unique=True, index=True)
    start_date = Column(Date)
    end_date = Column(Date)
    total_investment = Column(Numeric(10, 2))

    # Modify the relationship to include multiple legs
    legs = relationship("Option", back_populates="strategy", cascade="all, delete-orphan")  # Enable cascading delete for legs

    def add_leg(self, db, leg_data):
        # Method to add a leg to an OptionStrategy
        leg = Option(**leg_data, strategy_id=self.id)
        db.add(leg)
        db.commit()
        db.refresh(leg)
        return leg

    def remove_leg(self, db, leg_id):
        # Method to remove a leg from an OptionStrategy
        leg = db.query(Option).filter(Option.id == leg_id, Option.strategy_id == self.id).first()
        if leg:
            db.delete(leg)
            db.commit()
            return {"message": "Leg removed successfully"}
        return {"message": "Leg not found or not associated with this strategy"}


