import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import os
from io import StringIO

CACHE_FILE = "stock_performance_cache.json"
CSV_URL = "https://media.githubusercontent.com/media/leosmigel/analyzingalpha/master/2019-09-18-sp500-historical-components-and-changes/sp500_history.csv"
WIKI_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

def download_csv(url):
    response = requests.get(url)
    if response.status_code == 200:
        return StringIO(response.text)
    else:
        response.raise_for_status()

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as file:
            return json.load(file)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as file:
        json.dump(cache, file)

def parse_dates(date_str):
    # Try parsing the date with two possible formats
    try:
        return pd.to_datetime(date_str, format="%B %d, %Y")
    except ValueError:
        return pd.to_datetime(date_str, format="%Y-%m-%d %H:%M:%S")

def get_sp500_tickers_from_csv(year):
    csv_file = download_csv(CSV_URL)
    df = pd.read_csv(csv_file)

    # Convert 'date' column to datetime using custom parsing function
    df['date'] = df['date'].apply(parse_dates)

    # Filter for tickers up to the specified year
    df_filtered = df[df['date'].dt.year <= year]

    # Initialize an empty set to store the tickers
    tickers = set()

    # Iterate through the DataFrame to add or remove tickers
    for _, row in df_filtered.iterrows():
        if row['action'] == 'added':
            tickers.add(row['ticker'])
        elif row['action'] == 'removed' and row['ticker'] in tickers:
            tickers.remove(row['ticker'])

    return list(tickers)

def get_sp500_changes_from_wikipedia():
    response = requests.get(WIKI_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    changes_table = soup.find_all('table', {'class': 'wikitable'})[1]

    data = []
    rows = changes_table.find_all('tr')[1:]  # Skip header row
    for row in rows:
        cols = row.find_all(['th', 'td'])
        if len(cols) >= 5:
            date_str = cols[0].text.strip()
            added_ticker = cols[1].text.strip()
            removed_ticker = cols[3].text.strip()

            # Parsing date and year
            date = pd.to_datetime(date_str, errors='coerce')
            if pd.notnull(date):
                data.append((date, added_ticker, removed_ticker))

    return data

def get_sp500_tickers_from_wikipedia(year, changes_data):
    tickers = set()

    for date, added_ticker, removed_ticker in changes_data:
        if date.year <= year:
            if added_ticker:
                tickers.add(added_ticker)
            if removed_ticker:
                tickers.discard(removed_ticker)

    return list(tickers)

def get_sp500_tickers(year):
    # Get CSV tickers
    csv_tickers = get_sp500_tickers_from_csv(year)

    # Get Wikipedia changes data
    changes_data = get_sp500_changes_from_wikipedia()

    # Get Wikipedia tickers for the specified year
    wiki_tickers = get_sp500_tickers_from_wikipedia(year, changes_data)

    # Combine tickers, prioritizing Wikipedia data
    combined_tickers = list(set(csv_tickers + wiki_tickers))

    return combined_tickers

def get_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date, end=end_date)
    return hist

def calculate_performance(start_price, end_price):
    return (end_price - start_price) / start_price

def stock_existed_during_year(ticker, year):
    stock = yf.Ticker(ticker)
    try:
        info = stock.info
        if 'listing_date' in info:
            listing_date = info['listing_date']
            listing_year = int(listing_date.split('-')[0])
            return listing_year <= year
        return True  # If no listing date is available, assume it existed
    except:
        return False

def get_top_performing_stocks(year, N):
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"

    # Load cache
    cache = load_cache()

    # Get the S&P 500 tickers
    tickers = get_sp500_tickers(year)

    performances = []

    for ticker in tickers:
        cache_key = f"{ticker}_{year}"
        if cache_key in cache:
            performance = cache[cache_key]
        else:
            if not stock_existed_during_year(ticker, year):
                continue

            data = get_stock_data(ticker, start_date, end_date)
            if data.empty or len(data) < 2:
                continue

            start_price = data['Close'].iloc[0]
            end_price = data['Close'].iloc[-1]

            performance = calculate_performance(start_price, end_price)
            cache[cache_key] = performance

        performances.append((ticker, performance))

    # Save cache
    save_cache(cache)

    performances.sort(key=lambda x: x[1], reverse=True)
    return performances[:N]

def main():
    year = int(input("Enter the calendar year: "))
    top_n = int(input("Enter the number of top performing stocks to return: "))

    top_performing_stocks = get_top_performing_stocks(year, top_n)

    print(f"Top {top_n} performing stocks in S&P 500 for the year {year}:")
    for ticker, performance in top_performing_stocks:
        print(f"{ticker}: {performance*100:.2f}%")

if __name__ == "__main__":
    main()
