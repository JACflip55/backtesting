import yfinance as yf
import pickle

import statmuse

fn_cached_returns = 'cached_returns.pk'
try:
    with open(fn_cached_returns, 'rb') as fi:
        cached_returns = pickle.load(fi)
except:
    cached_returns = {}

### STRATEGY: INVEST IN THE TOP N STOCKS OF THE PREVIOUS YEAR ###
# For year X buy the top N stocks from year X-1, investing $1000 in each stock
# Calculate the total value of the portfolio at the end of that year

def calculate_strategy_return(starty, endy, n, verbose=False):
    stock_holdings = {}
    total_invested = 0
    for year in range(starty, endy + 1):
        # Get the top N stocks from the previous year
        top_n_stocks = get_top_n_stocks_prev_year(year, n)
        for stock in top_n_stocks:
            # Invest $1000 in each stock
            if stock not in stock_holdings:
                stock_holdings[stock] = 1000
            else:
                stock_holdings[stock] += 1000
            total_invested += 1000
        stock_holdings = update_portfolio(stock_holdings, year)
        portfolio_value = sum(stock_holdings.values())

    sorted_holdings = sorted(stock_holdings.items(), key=lambda x: x[1], reverse=True)
    total_return = portfolio_value - total_invested
    if verbose:
        print_summary(sorted_holdings, total_invested, portfolio_value)
    return total_return, portfolio_value / total_invested

def get_top_n_stocks_prev_year(year, n):
    top_n_stocks = statmuse.get_top_n_tickers(year - 1, n)
    return top_n_stocks

def print_summary(sorted_holdings, total_invested, portfolio_value):
    print("\n\n\n")
    print("Portfolio sorted by holdings:\n")
    for stock, value in sorted_holdings:
        print(f"{stock}: ${value:.2f}")
    print("\n\n\n")
    print(f"Total invested: ${total_invested:.2f}")
    print(f"Total return: ${portfolio_value - total_invested:.2f}")
    print(f"Final portfolio return multiplier: {portfolio_value / total_invested:.2f}")

def update_portfolio(portfolio, calendar_year):
    print(f"{calendar_year} Starting portfolio: {portfolio}...")
    new_portfolio = portfolio.copy()
    if calendar_year not in cached_returns:
        cached_returns[calendar_year] = {}
    for stock, amount_invested in portfolio.items():
        if stock in cached_returns[calendar_year].keys():
            price_multiplier = cached_returns[calendar_year][stock]
            if price_multiplier == 0:
                print(f"Assuming stock is now worthless. Removing {stock} from the portfolio...")
                print(f"Amount invested in {stock}: ${amount_invested:.2f} at beginning of year {calendar_year}.")
                new_portfolio.pop(stock)
                continue
            new_portfolio[stock] = (amount_invested * price_multiplier)
            continue
        try:
            print(f"Fetching data for {stock} in {calendar_year}...")
            data = yf.download(stock, start=f'{calendar_year}-01-01', end=f'{calendar_year}-12-31')
            if data.empty:
                print(f"No data found for {stock} in {calendar_year}")
                print(f"Assuming stock is now worthless. Removing {stock} from the portfolio...")
                print(f"Amount invested in {stock}: ${amount_invested:.2f} at beginning of year {calendar_year}.")
                new_portfolio.pop(stock)
                cached_returns[calendar_year][stock] = 0
                continue
            if not data.empty:
                end_price = data['Adj Close'].iloc[-1]
                start_price = data['Adj Close'].iloc[0]
                price_multiplier = end_price / start_price
                print(f"Price multiplier for {stock} in {calendar_year}: {price_multiplier}")
                new_portfolio[stock] = (amount_invested * price_multiplier)
                cached_returns[calendar_year][stock] = price_multiplier
        except Exception as e:
            print(f"Error calculating value for {stock} in {calendar_year}: {e}")
    print(f"{calendar_year} Ending portfolio: {new_portfolio}")
    return new_portfolio

def baseline_test(ticker, starty, endy):
    stock_holdings = {}
    total_invested = 0
    for year in range(starty, endy + 1):
        if ticker not in stock_holdings:
            stock_holdings[ticker] = 1000
        else:
            stock_holdings[ticker] += 1000
        total_invested += 1000
        print(f"Total portfolio value at the beginning of {year}: ${sum(stock_holdings.values()):.2f}")
        stock_holdings = update_portfolio(stock_holdings, year)
        portfolio_value = sum(stock_holdings.values())
        print(f"Total portfolio value at the end of {year}: ${portfolio_value:.2f}")
        print(f"Total invested: ${total_invested:.2f}")
        print(f"Total return: ${portfolio_value - total_invested:.2f}")
    print(f"Final portfolio return multiplier: {portfolio_value / total_invested:.2f}")
    return portfolio_value - total_invested, portfolio_value / total_invested

def run_experiment():
    periods = [(start, start + 19) for start in range(1962, 2024 - 19)]
    results = []

    for starty, endy in periods:
        print(f"Running experiment for {starty}-{endy}...")
        return_15, multiplier_15 = calculate_strategy_return(starty, endy, 15)
        return_20, multiplier_20 = calculate_strategy_return(starty, endy, 20)
        return_25, multiplier_25 = calculate_strategy_return(starty, endy, 25)
        baseline_return, baseline_multiplier = baseline_test("^GSPC", starty, endy)
        results.append((starty, endy, return_15, multiplier_15, return_20, multiplier_20, return_25, multiplier_25, baseline_return, baseline_multiplier))

    print_experiment_results(results)

def print_experiment_results(results):
    print("\n\n\n")
    print("Experiment Results:\n")
    for result in results:
        starty, endy, return_15, multiplier_15, return_20, multiplier_20, return_25, multiplier_25, baseline_return, baseline_multiplier = result
        print(f"Period: {starty}-{endy}")
        print(f"Top 15 stocks return: ${return_15:.2f}, Multiplier: {multiplier_15:.2f}")
        print(f"Top 20 stocks return: ${return_20:.2f}, Multiplier: {multiplier_20:.2f}")
        print(f"Top 25 stocks return: ${return_25:.2f}, Multiplier: {multiplier_25:.2f}")
        print(f"S&P 500 baseline return: ${baseline_return:.2f}, Multiplier: {baseline_multiplier:.2f}")
        best_portfolio = max([(multiplier_15, 'Top 15 stocks'), (multiplier_20, 'Top 20 stocks'), (multiplier_25, 'Top 25 stocks'), (baseline_multiplier, 'S&P 500 baseline')], key=lambda x: x[0])
        print(f"Best performing portfolio: {best_portfolio[1]} with percentage increase of: %${best_portfolio[0]*100:.2f}")
        print("\n")

# Run the experiment
run_experiment()

with open(fn_cached_returns, 'wb') as fi:
    pickle.dump(cached_returns, fi)
