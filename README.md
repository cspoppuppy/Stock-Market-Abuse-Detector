# Market Abuse Detection

-   Use traders data (csv files) and stocks data (Yahoo), analyse suspicious trades of one or more stock(s).

    -   Trades that happened in a non trading day of the stock
    -   Trades that outside of the price range of the day

-   Display susppicious traders (ranking table), and suspicious trades by country

-   Results are displayed using Flask.

-   #### Assumptions

    Bad data excluded from analysis:

    -   Traders data with no stockSymbol
    -   Traders data with no traderId
    -   Traders data with no tradeDatetime

    Ignored as suspicious:

    -   Traders data with missing price

### Setup

-   Prerequisite: Python3

-   Create virtual environment for this project

```console
virtualenv venv

# if virtualenv package not installed:
python3 -m venv venv
```

-   Activate virtual environment

```console
# MacOS / Unix
source venv/bin/activate


# Windows
venv\Scripts\activate.bat
```

-   Install dependencies

```console
pip install -r requirement.txt
```

### View analysis using Flask

```console
./run_server
```

Open in browser, url: http://127.0.0.1:5000/

### How to test

```console
python -m unittest discover tests
```

### How to use package (detector)

```python
from detector.analysis import Analysis

analysis = Analysis(filename=None, stock_symbols=[])
# Example 1: analysis on Amazon
analysis = Analysis("traders_data.csv", ["AMZN"])
# Example 2: analysis on all stocks
analysis = Analysis("traders_data.csv")

# Suspicious traders ranking
analysis.count_suspicious_per_trader()

# Suspicious trades by country
analysis.count_suspicious_by_country_per_month()
```
