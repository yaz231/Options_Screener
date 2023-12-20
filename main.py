import models
from yahoo_fin import options as op, stock_info as si
import re
import pandas as pd
from datetime import datetime, timedelta
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Option

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

database = {}

templates = Jinja2Templates(directory="templates")

class StockRequest(BaseModel):
    symbol: str
    date: str

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def home(request: Request, ticker_name = None, exp_date = None, contract_type = None, in_the_money = None, db: Session = Depends(get_db)):
    """
    displays the stock screener dashboard / homepage
    :return:
    """
    options = db.query(Option)
    expiration_dates = get_expiration_dates()

    if ticker_name:
        print(f"Ticker Name: {ticker_name}")
        options = options.filter(Option.symbol == ticker_name)

        if in_the_money:  # Added filter for in the money options
            in_the_money = bool(in_the_money)
            print(f"In the Money: {in_the_money}")
            current_price = si.get_live_price(ticker_name).round(2)
            if contract_type == 'Puts':
                options = options.filter(Option.strike > current_price)
            else:
                options = options.filter(Option.strike < current_price)


    if exp_date:
        if len(exp_date) > 1:
            exp_date = expiration_dates.index(exp_date)
        print(f"Expiration Date: {expiration_dates[int(exp_date)]}")
        date_object = datetime.strptime(expiration_dates[int(exp_date)], "%B %d, %Y")
        converted_date = date_object.strftime("%Y-%m-%d")
        options = options.filter(Option.exp_date == converted_date)

    if contract_type:
        print(f"Contract Type: {contract_type}")
        if contract_type == 'Puts':
            options = options.filter(Option.type == "Put")
        else:
            options = options.filter(Option.type == "Call")

    # if in_the_money:  # Added filter for in the money options
    #     print(f"In the Money: {in_the_money}")
    #     current_price = si.get_live_price(ticker_name).round(2)
    #     if contract_type == 'Puts':
    #         options = options.filter(Option.strike > current_price)
    #     else:
    #         options = options.filter(Option.strike < current_price)

    # print(exp_dates)
    return templates.TemplateResponse("home.html", context={
        "request": request,
        "options": options,
        "expiration_dates": expiration_dates,
        "ticker_name": ticker_name,
        "exp_date": expiration_dates[int(exp_date)] if exp_date else expiration_dates[0],
        "contract_type": contract_type if contract_type else "Type",
        "in_the_money": in_the_money
    })

def find_expiration(week=0):
    today = datetime.today()
    days_to_friday = (4 - today.weekday()) % 7
    expiration_date = (today + timedelta(days=days_to_friday + 7*week)).strftime('%Y-%m-%d')
    return expiration_date

def get_expiration_dates():
    return op.get_expiration_dates('TSLA')[:8]

def reformat_df(df, puts = True):
    df.insert(0, 'Symbol', re.search(r'\D+', df['Contract Name'].iloc[0]).group())
    if puts:
        df.insert(1, 'Type', 'Put')
    else:
        df.insert(1, 'Type', 'Call')
    df = df.drop(columns=["Contract Name", "Last Trade Date"])
    return df

def fetch_option_data(ticker: str, date: str, db: Session):
    date_object = datetime.strptime(date, "%B %d, %Y")
    expiration_date = date_object.strftime("%Y-%m-%d")

    df1 = reformat_df(op.get_puts(ticker, expiration_date), puts=True)
    df2 = reformat_df(op.get_calls(ticker, expiration_date), puts=False)
    df = pd.concat([df1, df2])

    if len(df) == 0:
        return

    date_object = datetime.strptime(expiration_date, "%Y-%m-%d").date()

    current_price = si.get_live_price(df['Symbol'].iloc[0]).round(2)
    df['Implied Volatility'] = df['Implied Volatility'].str.translate(str.maketrans({'%': '', ',': ''}))
    df = df.drop(columns=['Bid', 'Ask', 'Change', '% Change', 'Volume'])

    for index, row in df.iterrows():
        # Query the database for an existing entry with the same symbol and expiration date
        existing_option = db.query(Option).filter(
            Option.symbol == row['Symbol'],
            Option.exp_date == date_object
        ).first()

        if existing_option:
            # Update the attributes of the existing entry with the new data
            existing_option.current_price = current_price
            existing_option.strike = row['Strike']
            existing_option.type = row['Type']
            existing_option.premium = row['Last Price']
            existing_option.open_interest = row['Open Interest']
            existing_option.implied_volatility = row['Implied Volatility']
        else:
            # Create a new option entry
            option = Option(
                symbol=row['Symbol'],
                current_price=current_price,
                strike=row['Strike'],
                exp_date=date_object,
                type=row['Type'],
                premium=row['Last Price'],
                open_interest=row['Open Interest'],
                implied_volatility=row['Implied Volatility']
            )
            db.add(option)

    db.commit()
    db.close()


@app.post("/stock")
async def create_stock(stock_request: StockRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Created a stock and stores it in the database
    :return:
    """

    background_tasks.add_task(fetch_option_data, stock_request.symbol, stock_request.date, db)

    return {"code": "success",
            "message": "Stock Ticker was added to the database"
    }

@app.post("/delete_all")
def delete_all_records(db: Session = Depends(get_db)):
  """
  Deletes all records from the database.
  """
  try:
    # Delete all records from the database using your ORM or database library
    db.query(Option).delete()
    db.commit()
    return {"code": "success", "message": "All records deleted successfully."}
  except Exception as e:
    # Handle the deletion failure case
    db.rollback()
    return {"code": "error", "message": str(e)}