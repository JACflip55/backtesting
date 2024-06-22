import yfinance as yf
import pickle

import statmuse

fn_cached_returns = '__pycache__/cached_returns.pk'
try:
    with open(fn_cached_returns, 'rb') as fi:
        cached_returns = pickle.load(fi)
except:
    cached_returns = {}

### STRATEGY: INVEST IN THE TOP 20 STOCKS OF THE PREVIOUS YEAR ###
# For year X buy the top 20 stocks from year X-1 Investing $1000 in each stock
# Calculate the total value of the portfolio at the end of that year

# For the first 10 years we could only invest 500 in each stock and for the next 10 years we could invest 1000 in each stock. This is more realistic as we would have more money to invest as time goes on.

def calculate_strategy_return(starty, endy, verbose=False, n=20, amount_to_invest=1000):
    stock_holdings = {}
    total_invested = 0
    for year in range(starty, endy+1):
        # Get the top 20 stocks from the previous year
        top_20_stocks = get_top_stocks_prev_year(year, n)
        for stock in top_20_stocks:
            # Invest $1000 in each stock
            if stock not in stock_holdings:
                stock_holdings[stock] = amount_to_invest
            else:
                stock_holdings[stock] += amount_to_invest
            total_invested += amount_to_invest
        # print(f"Total portfolio value at the beginning of {year}: ${sum(stock_holdings.values()):.2f}")
        stock_holdings = update_portfolio(stock_holdings, year)
        portfolio_value = sum(stock_holdings.values())
        # print(f"Total portfolio value at the end of {year}: ${portfolio_value:.2f}")

    sorted_holdings = sorted(stock_holdings.items(), key=lambda x: x[1], reverse=True)
    total_return = portfolio_value - total_invested
    if verbose:
        print_summary( sorted_holdings, total_invested, portfolio_value)
    return (total_return, sorted_holdings)

# This might not be right, but if we trust the data at the top of the file
def get_top_stocks_prev_year(year, n):
    top_stocks = statmuse.get_top_n_tickers(year - 1, n)
    return top_stocks

def print_summary(sorted_holdings, total_invested, portfolio_value):
    # Print the final summary
    print("\n\n\n")
    print("\n\n\n")
    print("Portfolio sorted by holdings:\n")
    for stock, value in sorted_holdings:
        print(f"{stock}: ${value:.2f}")
    print("\n\n\n")
    print(f"Total invested: ${total_invested:.2f}")
    print(f"Total return: ${portfolio_value - total_invested:.2f}")
    print(f"Final portfolio return multiplier: {portfolio_value / total_invested:.2f}")

# portfolio is a dictionary with stock tickers as keys and the amount invested in each stock as values
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


# BASELINE: INVEST IN THE S&P 500 INDEX ###
# For year X invest $1000 in the S&P 500 index
# Calculate the total value of the portfolio at the end of that year
def baseline_test(ticker, starty, endy):
    stock_holdings = {}
    total_invested = 0
    for year in range(starty, endy+1):
        # Get the top 20 stocks from the previous year
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
    return stock_holdings

# calculate_strategy_return(1961, 1980, verbose=True)
# baseline_test("^GSPC", 1961, 1980)
# calculate_strategy_return(1981, 2000, verbose=True)
# baseline_test("^GSPC", 1981, 2000)
calculate_strategy_return(2001, 2020, verbose=True)
baseline_test("BRK-A", 2001, 2020)
#baseline_test("^GSPC", 2001, 2020)


with open(fn_cached_returns, 'wb') as fi:
    pickle.dump(cached_returns, fi)

