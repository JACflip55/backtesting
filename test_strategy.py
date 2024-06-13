import yfinance as yf

# Example tickers for earlier years. Update this list with appropriate historical tickers.
# Assume that these are the stocks to buy for a specific year.
# AKA the top performers for the PRIOR year

sp500_tickers = {
    1985: ['HAS', 'USB', 'TSN', 'MCD', 'BALL', 'ED', 'VZ', 'BA', 'CNP', 'VTRS', 'K', 'D', 'BEN', 'BMY', 'NOC', 'AEP', 'KO', 'GD', 'DHR', 'KEY'],  # Example tickers from 1984
    1986: ['HRL', 'BEN', 'USB', 'L', 'CHD', 'AMGN', 'UNH', 'BBWI', 'BIO', 'WRB', 'TSN', 'BRO', 'BK', 'BBY', 'VLO', 'PAYX', 'VMC', 'ADSK', 'AOS', 'MCD'],  # Example tickers from 1985
    1987: ['NKE', 'HRL', 'FMC', 'KO', 'USB', 'ITW', 'TSN', 'VMC', 'MSFT', 'ADBE', 'JBHT', 'MRK', 'AAPL', 'PAYX', 'MMC', 'MDT', 'WDC', 'JCI', 'MO', 'BEN'],  # Example tickers from 1986
    1988: ['NKE', 'MU', 'ORCL', 'USB', 'MSFT', 'ADBE', 'AAPL', 'AMAT', 'J', 'INTC', 'NEM', 'RHI', 'ADSK', 'NDSN', 'DD', 'HD', 'KO', 'TT', 'DE', 'LRCX'],  # Example tickers from 1987
    1989: ['USB', 'ROST', 'MO', 'DVN', 'FAST', 'MOS', 'CDNS', 'COST', 'CMS', 'ETR', 'CAH', 'HD', 'NI', 'BA', 'TJX', 'ADBE', 'VLO', 'TROW', 'JPM', 'JCI'],  # Example tickers from 1988
    1990: ['DVN', 'UNH', 'NKE', 'VTRS', 'KO', 'ORCL', 'COST', 'APA', 'CHD', 'SCHW', 'CPB', 'BEN', 'GL', 'SYK', 'CDNS', 'MKC', 'CAH', 'BKR', 'OKE', 'HUM'],  # Example tickers from 1989
    1991: ['WM', 'NKE', 'CNMD', 'AMGN', 'TECH', 'DGII', 'PDEX', 'TARO', 'CSCO', 'RRC', 'POWL', 'UNH', 'DXLG', 'VICR', 'J', 'BCPC', 'PLAB', 'MTH', 'MSFT', 'MGRC'],  # Example tickers from 1990
    1992: ['JKHY', 'TECH', 'EA', 'SCHW', 'AMGN', 'PTC', 'AMD', 'SYK', 'GEN', 'UNH', 'WM', 'CSCO', 'BBY', 'LH', 'ROST', 'HAS', 'LRCX', 'HD', 'PHM', 'TER'],  # Example tickers from 1991
    1993: ['WDC', 'JKHY', 'STE', 'CSCO', 'BBY', 'AOS', 'EA', 'GD', 'MNST', 'ORCL', 'AMAT', 'BK', 'JPM', 'PTC', 'INTC', 'NUE', 'SBUX', 'LUV', 'CINF', 'ADI'],  # Example tickers from 1992
    1994: ['CRMT', 'AVNW', 'MCHP', 'PTSI', 'AAON', 'ASXC', 'CULP', 'DIOD', 'ROP', 'AU', 'CDZI', 'SKYW', 'GNTX', 'AGCO', 'WSM', 'DYNT', 'AEM', 'LNW', 'MODG', 'ASYS'],  # Example tickers from 1993
    1995: ['LSTA', 'MICS', 'FRHC', 'SLNH', 'IDCC', 'DLHC', 'CSBR', 'SEEL', 'CMCL', 'PRPH', 'DYNT', 'FLL', 'BMRA', 'CYTH', 'FIZZ', 'EP', 'GIII', 'COO', 'DIOD', 'NTIC'],  # Example tickers from 1994
    1996: ['BIIB', 'REGN', 'GILD', 'CDNS', 'BSX', 'HOLX', 'JBL', 'IDXX', 'JKHY', 'IT', 'ROST', 'INTU', 'CI', 'SWKS', 'CSCO', 'NKE', 'ADBE', 'FAST', 'MDT', 'AMGN'],  # Example tickers from 1995
    1997: ['JBL', 'WDC', 'ROST', 'TJX', 'COO', 'INTC', 'DLTR', 'AES', 'TROW', 'POOL', 'INCY', 'NKE', 'CVS', 'MSFT', 'EXPD', 'CSCO', 'WM', 'WAT', 'RMD', 'PCAR'],  # Example tickers from 1996
    1998: ['BBY', 'TYL', 'APH', 'COO', 'RCL', 'CINF', 'CZR', 'LEN', 'JBL', 'AMZN', 'SWKS', 'WAB', 'AES', 'RJF', 'SCHW', 'USB', 'FITB', 'BEN', 'MCK', 'IVZ'],  # Example tickers from 1997
    1999: ['AMZN', 'EBAY', 'QRVO', 'BBY', 'RMD', 'CTSH', 'AAPL', 'MNST', 'VRSN', 'NTAP', 'CSCO', 'WAT', 'SWKS', 'NVR', 'LOW', 'MSFT', 'COF', 'SCHW', 'HD', 'WMT'],  # Example tickers from 1998
    2000: ['QCOM', 'VRSN', 'FFIV', 'LRCX', 'QRVO', 'BIIB', 'ORCL', 'CTSH', 'NTAP', 'JNPR', 'TER', 'ADI', 'AKAM', 'TRMB', 'AMAT', 'GLW', 'ADBE', 'GEN', 'CSGP', 'LH'],  # Example tickers from 1999
    2001: ['LH', 'DGX', 'VRTX', 'COR', 'EOG', 'EG', 'WAT', 'UHS', 'REGN', 'NVR', 'RVTY', 'DVA', 'CB', 'HSIC', 'TDY', 'MET', 'BLK', 'MO', 'JKHY', 'UNH'],  # Example tickers from 2000
    2002: ['KMX', 'BKNG', 'NVDA', 'TSCO', 'CZR', 'AZO', 'BBY', 'TYL', 'WDC', 'GPN', 'FFIV', 'ANSS', 'LOW', 'MHK', 'EBAY', 'BIO', 'WRK', 'AXON', 'GEN', 'ROST'],  # Example tickers from 2001
    2003: ['TSCO', 'ODFL', 'BSX', 'CTSH', 'AMZN', 'TPR', 'NVR', 'NEM', 'CNC', 'HAL', 'BALL', 'TTWO', 'AOS', 'GRMN', 'ZBH', 'STE', 'HOLX', 'ROST', 'ROL', 'FCX'],  # Example tickers from 2002
    2004: ['AXON', 'DECK', 'AKAM', 'ALGN', 'WMB', 'NFLX', 'ON', 'AES', 'GLW', 'TRMB', 'LRCX', 'AMZN', 'JNPR', 'FCX', 'DHI', 'TYL', 'FFIV', 'LEN', 'AMD', 'HUM'],  # Example tickers from 2003
    2005: ['AXON', 'DECK', 'AKAM', 'ALGN', 'WMB', 'NFLX', 'ON', 'AES', 'GLW', 'TRMB', 'LRCX', 'AMZN', 'JNPR', 'FCX', 'DHI', 'TYL', 'FFIV', 'LEN', 'AMD', 'HUM'],  # Example tickers from 2004
}

### STRATEGY: INVEST IN THE TOP 20 STOCKS OF THE PREVIOUS YEAR ###
# For year X buy the top 20 stocks from year X-1 Investing $1000 in each stock
# Calculate the total value of the portfolio at the end of that year

def calculate_strategy_return(starty, endy):
    stock_holdings = {}
    total_invested = 0
    for year in range(starty, endy+1):
        # Get the top 20 stocks from the previous year
        # top_20_stocks = get_top_20_stocks(year - 1)
        top_20_stocks = get_top_20_stocks_prev_year(year)
        for stock in top_20_stocks:
            # Invest $1000 in each stock
            if stock not in stock_holdings:
                stock_holdings[stock] = 1000
            else:
                stock_holdings[stock] += 1000
            total_invested += 1000
        print(f"Total portfolio value at the beginning of {year}: ${sum(stock_holdings.values()):.2f}")
        stock_holdings = update_portfolio(stock_holdings, year)
        portfolio_value = sum(stock_holdings.values())
        print(f"Total portfolio value at the end of {year}: ${portfolio_value:.2f}")

    # Print the final summary
    print("\n\n\n")
    print("\n\n\n")
    print("Portfolio sorted by holdings:\n")
    sorted_holdings = sorted(stock_holdings.items(), key=lambda x: x[1], reverse=True)
    for stock, value in sorted_holdings:
        print(f"{stock}: ${value:.2f}")
    print("\n\n\n")
    print(f"Total invested: ${total_invested:.2f}")
    print(f"Total return: ${portfolio_value - total_invested:.2f}")
    print(f"Final portfolio return multiplier: {portfolio_value / total_invested:.2f}")

    return stock_holdings

# This might not be right, but if we trust the data at the top of the file
def get_top_20_stocks_prev_year(year):
    top_20_stocks = sp500_tickers.get(year, [])
    return top_20_stocks

# portfolio is a dictionary with stock tickers as keys and the amount invested in each stock as values
def update_portfolio(portfolio, calendar_year):
    print(f"{calendar_year} Starting portfolio: {portfolio}...")
    new_portfolio = portfolio.copy()
    for stock, amount_invested in portfolio.items():
        try:
            print(f"Fetching data for {stock} in {calendar_year}...")
            data = yf.download(stock, start=f'{calendar_year}-01-01', end=f'{calendar_year}-12-31')
            if data.empty:
                print(f"No data found for {stock} in {calendar_year}")
                print(f"Assuming stock is now worthless. Removing {stock} from the portfolio...")
                print(f"Amount invested in {stock}: ${amount_invested:.2f} at beginning of year {calendar_year}.")
                new_portfolio.pop(stock)
                continue
            if not data.empty:
                end_price = data['Adj Close'].iloc[-1]
                start_price = data['Adj Close'].iloc[0]
                price_multiplier = end_price / start_price
                print(f"Price multiplier for {stock} in {calendar_year}: {price_multiplier}")
                new_portfolio[stock] = (amount_invested / start_price) * end_price
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

# baseline_test("^GSPC", 1985, 2005) # 285% value increase
# baseline_test('SPY', 1993, 2005) # Does not exist until 93 - 179% return
# baseline_test("^GSPC", 1993, 2005) # 161% cash increase
# baseline_test('HRL', 1985, 2005) # 504% cash increase
calculate_strategy_return(1985, 2005) # 1243% return
# Total portfolio value at the end of 2004: $4970954.92
# Total invested: $400000.00
# Total return: $4570954.92

# baseline_test('SPY', 1985, 2005)
# baseline_test("^GSPC", 2005, 2020)
# baseline_test('SPY', 2005, 2020)

