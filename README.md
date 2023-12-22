# Option Screener

Option Screener is a web application that allows users to filter and view options data for stocks based on various criteria.
It also allows you to view and compare different stocks all on the same screen.

Disclaimer: This project is mostly used to explore different concepts when developing a web application. This project is still under development and will undergo changes but for now I like where it is. 
## Installation

1. Clone the repository.

    ```bash
    git clone https://github.com/yaz231/Options_Screener.git
    cd Options_Screener
    ```

2. Set up a virtual environment (optional but recommended).

    ```bash
    python -m venv env
    source venv/bin/activate  # For Unix/Linux
    .\env\Scripts\activate   # For Windows
    ```

3. Install dependencies.

    ```bash
    pip install -r requirements.txt
    ```

## Running the Project

To run the project, use the following command:

```bash
uvicorn main:app --reload
```
## Using the Project
### Options Screener
The first screen allows you to add company tickers to a local database that shows you the Stock Ticker, the Current Price, the Expiration Date, the Type of Contract (Calls or Puts), the Strike Price, the Premium, the Open Interest, and the Implied Volatility.
You also have the ability to filter the database based on what contracts you might be searching for! After Adding Stocks or Filtering, please refresh the page to see the updated table.

### Stock Chart
Clicking on the Stock Chart will navigate you to the Stock Chart page. This page will show all the stocks added to your database in the same graph. Additionally, on the right side, you'll be able to see the percentage change for each stock for the given time period.
The Time Period can be changed between 1 Year, 6 Months, 3 Months, 1 Month, and 1 Week.

Enjoy and let me know what changes I can make!
