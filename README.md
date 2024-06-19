# Backtesting
Backtesting Investment Strategies

## Directions

To run the experiment first ensure all packages are installed (beautifulsoup4, yfinance), then run `python backtesting_experiment.py`

The first run will be slow because it has to pull data from statmuse and yfinance.

Subsequent runs will be much faster due to data in the cache.

## Future Work

Things that it would be interesting to test that should be possible with the data available:
1. Varying the lookback time (ex. best performing stocks over past 2 or 3 years instead of 1).
1. Varying the purchase frequency. (ex. we could purchase stocks every 9 or 18 months instead of every year.
1. Try purchasing on a different day than Jan 1. (ex. mid december).
1. Consider excluding the top performing N stocks. (ex. buy the top 25 performers but not the top 3 performers in any given year)
