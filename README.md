# Option Screener

Option Screener is a web application that allows users to filter and view options data for stocks based on various criteria.

## Installation

1. Clone the repository.

    ```bash
    git clone <repository_url>
    cd option-screener
    ```

2. Set up a virtual environment (optional but recommended).

    ```bash
    python -m venv env
    source env/bin/activate  # For Unix/Linux
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
