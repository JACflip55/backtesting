# Backtesting
Backtesting Investment Strategies

## Directions

Install the dependencies, then run the experiment:

```
pip install -r requirements.txt
python run_experiment.py
```

The first run will be slow because it has to pull data from statmuse and yfinance.

Subsequent runs will be much faster due to data in the cache.

In order to see the detailed breakdown of a specific portfolio for a specific period you can run `python test_strategy.py`

You can also run the statmuse file to explore the data a little bit, or `streamlit run app.py` for a small web UI.

The strategy maths has unit tests that need no network access:

```
python -m unittest discover -s tests
```

## Known issue

StatMuse now renders its result tables in the browser, so `statmuse.py` can no longer scrape the
yearly top and bottom performers from the page HTML. Years that are already in the local cache
still work; years that are not come back empty.

## Future Work

Things that it would be interesting to test that should be possible with the data available:
1. Unify the `backtesting_experiment` and `test_strategy` files as there is a lot of repeated code.
2. Varying the lookback time (ex. best performing stocks over past 2 or 3 years instead of 1).
3. Varying the purchase frequency. (ex. we could purchase stocks every 9 or 18 months instead of every year.
4. Try purchasing on a different day than Jan 1. (ex. mid december).
5. Consider excluding the top performing N stocks. (ex. buy the top 25 performers but not the top 3 performers in any given year)
6. Selling a stock if it has 2 out of 3 negative years
7. Explore and validate additional data sources.
