import yfinance as yf
import pandas as pd

# Example tickers for earlier years. Update this list with appropriate historical tickers.
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

def get_top_20_stocks(year):
    performance = {}
    tickers = sp500_tickers.get(year, [])

    for ticker in tickers:
        try:
            data = yf.download(ticker, start=f'{year}-01-01', end=f'{year}-12-31')
            if not data.empty:
                start_price = data['Adj Close'].iloc[0]
                end_price = data['Adj Close'].iloc[-1]
                annual_return = (end_price - start_price) / start_price
                performance[ticker] = annual_return
        except Exception as e:
            print(f"Error fetching data for {ticker} in {year}: {e}")

    top_20_stocks = sorted(performance, key=performance.get, reverse=True)[:20]
    return top_20_stocks

def calculate_historical_returns():
    investment_per_stock = 1000
    total_value_over_time = []

    # Initialize a dictionary to hold the amount of money invested in each stock
    stock_holdings = {}

    for year in range(1985, 2006):
        top_20_stocks = get_top_20_stocks(year)
        if not top_20_stocks:
            print(f"No top stocks found for the year {year}")
            continue

        # Invest in the top 20 stocks of the previous year
        for stock in top_20_stocks:
            if stock not in stock_holdings:
                stock_holdings[stock] = 0
            stock_holdings[stock] += investment_per_stock

        # Calculate the current value of the portfolio
        current_value = 0
        for stock, amount_invested in stock_holdings.items():
            try:
                data = yf.download(stock, start=f'{year}-01-01', end=f'{year}-12-31')
                if not data.empty:
                    end_price = data['Adj Close'].iloc[-1]
                    current_value += (amount_invested / data['Adj Close'].iloc[0]) * end_price
            except Exception as e:
                print(f"Error calculating value for {stock} in {year}: {e}")

        total_value_over_time.append((year, current_value))

    return total_value_over_time

# Run the function and print the historical returns
historical_returns = calculate_historical_returns()
for year, value in historical_returns:
    print(f"Total portfolio value at the end of {year}: ${value:.2f}")
