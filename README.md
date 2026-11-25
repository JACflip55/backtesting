# Backtesting 📈

Backtest investment strategies against historical stock performance data. Tests whether buying top-performing stocks from the prior year and holding them beats the market — and by how much.

Built with Python, yfinance, and StatMuse data. Includes a Streamlit web UI for exploring results.

## Quick start

```bash
pip install -r requirements.txt
python run_experiment.py
```

The first run will be slow because it has to pull data from StatMuse and yfinance. Subsequent runs use the local cache.

## Usage

| Command | What it does |
|---------|-------------|
| `python run_experiment.py` | Run the full backtest across all years |
| `python test_strategy.py` | Detailed breakdown for a specific portfolio/period |
| `streamlit run app.py` | Launch the web UI |
| `python -m unittest discover -s tests` | Run unit tests (no network needed) |

## Data source note

StatMuse rate-limits unauthenticated visitors after a few page views, then shows a sign-in prompt. When that happens, `statmuse.py` raises `StatMuseLimitReached` instead of continuing with missing data. Years already in the local cache are unaffected — a full multi-decade experiment builds up over several sessions.

**Use only the cached data. Do not repeatedly scrape the providers.**

## Future work

1. Unify `backtesting_experiment` and `test_strategy` (lots of shared code)
2. Vary the lookback window (2-3 years instead of 1)
3. Vary purchase frequency (every 9 or 18 months)
4. Try different entry dates (mid-December instead of Jan 1)
5. Exclude the very top performers (buy top 25 but skip top 3)
6. Sell after 2 out of 3 negative years
7. Explore additional data sources

## License

MIT
