import os
import pickle

import yfinance as yf

import statmuse

fn_cached_returns = '__pycache__/cached_returns.pk'
try:
    with open(fn_cached_returns, 'rb') as fi:
        cached_returns = pickle.load(fi)
except (FileNotFoundError, EOFError, pickle.UnpicklingError):
    cached_returns = {}


def save_cached_returns():
    """Write the yearly price multipliers fetched so far back to the cache file."""
    os.makedirs(os.path.dirname(fn_cached_returns), exist_ok=True)
    with open(fn_cached_returns, 'wb') as fi:
        pickle.dump(cached_returns, fi)

annual_investment_total = 20000  # Total amount to invest each year

### STRATEGY: INVEST IN THE TOP N STOCKS OF THE PREVIOUS YEAR ###
# For year X buy the top N stocks from year X-1, investing $1000 in each stock
# Then, calculate the total value of the portfolio at the end of that year

def calculate_strategy_return(starty, endy, n, verbose=False, worst=False):
    stock_holdings = {}
    total_invested = 0
    annual_percentage_returns = {}
    for year in range(starty, endy + 1):
        initial_portfolio_value = sum(stock_holdings.values())
        # Get the top N stocks from the previous year
        if worst:
            stocks = get_bottom_n_stocks_prev_year(year, n)
        else:
            stocks = get_top_n_stocks_prev_year(year, n)
        for stock in stocks:
            # Invest $1000 in each stock
            if stock not in stock_holdings:
                stock_holdings[stock] = (annual_investment_total / n)
            else:
                stock_holdings[stock] += (annual_investment_total / n)
        total_invested += annual_investment_total
        stock_holdings = update_portfolio(stock_holdings, year)
        eoy_portfolio_value = sum(stock_holdings.values())
        base = initial_portfolio_value + annual_investment_total
        percentage_return = (eoy_portfolio_value - base) / base
        annual_percentage_returns[year] = percentage_return

    final_portfolio_value = sum(stock_holdings.values())
    sorted_holdings = sorted(stock_holdings.items(), key=lambda x: x[1], reverse=True)
    total_return = final_portfolio_value - total_invested
    average_annual_return = sum(annual_percentage_returns.values()) / len(annual_percentage_returns)
    if verbose:
        print_summary(sorted_holdings, total_invested, final_portfolio_value, annual_percentage_returns)
        return average_annual_return, total_return, final_portfolio_value / total_invested, sorted_holdings
    return average_annual_return, total_return, final_portfolio_value / total_invested

def get_top_n_stocks_prev_year(year, n):
    top_n_stocks = statmuse.get_top_n_tickers(year - 1, n)
    return top_n_stocks

def get_bottom_n_stocks_prev_year(year, n):
    bottom_n_stocks = statmuse.get_bottom_n_tickers(year - 1, n)
    return bottom_n_stocks

def print_summary(sorted_holdings, total_invested, portfolio_value, annual_percentage_returns, average_annual_return=None):
    print("\n\n\n")
    print("Portfolio sorted by holdings:\n")
    for stock, value in sorted_holdings:
        print(f"{stock}: ${value:.2f}")
    print("\n\n\n")
    print(f"Total invested: ${total_invested:.2f}")
    print(f"Total return: ${portfolio_value - total_invested:.2f}")
    print(f"Annual returns:")
    for year, percentage_return in annual_percentage_returns.items():
        print(f"{year}: {percentage_return:.2f}")
    print("\n\n\n")
    print("Average annual return:")
    print(f"Final portfolio return multiplier: {portfolio_value / total_invested:.2f}")

def update_portfolio(portfolio, calendar_year, verbose=False):
    if verbose:
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
            # auto_adjust=False keeps the 'Adj Close' column and multi_level_index=False keeps plain column
            # names; current yfinance versions changed both defaults.
            data = yf.download(stock, start=f'{calendar_year}-01-01', end=f'{calendar_year}-12-31',
                               auto_adjust=False, multi_level_index=False, progress=False)
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
    if verbose:
        print(f"{calendar_year} Ending portfolio: {new_portfolio}")
    return new_portfolio

def baseline_test(ticker, starty, endy):
    stock_holdings = {}
    total_invested = 0
    aprs = []
    for year in range(starty, endy + 1):
        if ticker not in stock_holdings:
            stock_holdings[ticker] = annual_investment_total
        else:
            stock_holdings[ticker] += annual_investment_total
        total_invested += annual_investment_total
        base = stock_holdings[ticker]
        print(f"Total portfolio value at the beginning of {year}: ${sum(stock_holdings.values()):.2f}")
        stock_holdings = update_portfolio(stock_holdings, year)
        portfolio_value = sum(stock_holdings.values())
        percentage_return = (portfolio_value - base) / base
        aprs.append(percentage_return)
        print(f"Total portfolio value at the end of {year}: ${portfolio_value:.2f}")
        print(f"Total invested: ${total_invested:.2f}")
        print(f"Total return: ${portfolio_value - total_invested:.2f}")
    print(f"Final portfolio return multiplier: {portfolio_value / total_invested:.2f}")
    avg_apr = sum(aprs) / len(aprs)
    return avg_apr, portfolio_value - total_invested, portfolio_value / total_invested

def compound_interest_calculator(percentage, num_years, verbose=False):
    portfolio_value = 0
    total_invested = 0

    for year in range(0, num_years):
        portfolio_value += annual_investment_total
        total_invested += annual_investment_total
        if verbose:
            print(f"Total portfolio value at the beginning of {year}: ${portfolio_value:.2f}")
        portfolio_value *= (1 + percentage)
        if verbose:
            print(f"Total portfolio value at the end of {year}: ${portfolio_value:.2f}")
        if verbose:
            print(f"Total invested: ${total_invested:.2f}")
            print(f"Total return: ${portfolio_value - total_invested:.2f}")
    if verbose:
      print(f"Final portfolio return multiplier: {portfolio_value / total_invested:.2f}")
    return portfolio_value - total_invested, portfolio_value / total_invested
