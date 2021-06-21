# Market Abuse Detection

In this task we need to retrieve stock data for Amazon and analyse some client 
data in order to find some suspicious behaviours. 

## Data description
- The file `traders_data.csv` includes some traders orders data. All those trades only reflect order
submissions, which may have been filled or not.
- Amazon stock data should be retrieved from Yahoo for the months of February and March 2020
using the library `pandas_datareader`. 

## Task
We want to find traders which made suspicious orders. To be a suspicious orders we consider the 
following rules:
- The trader has submitted an order above the high price/below the low price for a given day of a stock
- The trader has submitted an order in a date when the stock was not traded

If any suspicious orders are found, we want to do the following analysis:

- If more than one trader is found, rank by number of suspicious orders per trader.
- Try to find if there is a correlation between the nationality of the trader and the 
tendency to make suspicious orders 

## What is evaluated
- Code logic/functionality (use of Pandas) 
- Organisation of the code (python modules) 
- Performance considerations
- Data processing/cleaning
- Documentation (mainly docstrings) Testing (unittests or pytest)