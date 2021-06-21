# Market Abuse Detection

Analyse suspicious trades using traders data and stocks data.

Analysis are displayed using Flask.

### Assumptions

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

### How to use package

```python
from detector.analysis import Analysis

analysis = Analysis(filename=None, stock_symbols=[])
# I.e.
analysis = Analysis("traders_data.csv", ["AMZN"])

# Suspicious traders ranking
analysis.count_suspicious_per_trader()

# Suspicious trades by country
analysis.count_suspicious_by_country_per_month()
```
