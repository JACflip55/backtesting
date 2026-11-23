import os
import pickle
import re

import requests
from bs4 import BeautifulSoup

CACHE_DIR = '__pycache__'

def save_cache(data, year, stock_symbol=None):
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    filename = f'{stock_symbol}_{year}.pkl' if stock_symbol else f'{year}.pkl'
    cache_path = os.path.join(CACHE_DIR, filename)
    with open(cache_path, 'wb') as cache_file:
        pickle.dump(data, cache_file)

def load_cache(year, stock_symbol=None):
    filename = f'{stock_symbol}_{year}.pkl' if stock_symbol else f'{year}.pkl'
    cache_path = os.path.join(CACHE_DIR, filename)
    if os.path.exists(cache_path):
        with open(cache_path, 'rb') as cache_file:
            return pickle.load(cache_file)
    return None

def parse_ranking_table(page_html):
    """Return [[name, year, percent_return], ...] from a StatMuse ranking page.

    The table is found by its structure (the first table body whose rows have at
    least three cells) rather than by CSS class, because the site's class names change.
    """
    soup = BeautifulSoup(page_html, 'html.parser')
    for tbody in soup.find_all('tbody'):
        data = []
        for row in tbody.find_all('tr'):
            columns = row.find_all('td')
            if len(columns) < 3:
                continue
            name = columns[0].get_text(strip=True)
            year_fetched = columns[1].get_text(strip=True)
            percentage = columns[2].get_text(strip=True).replace('%', '').replace(',', '')
            try:
                data.append([name, year_fetched, float(percentage)])
            except ValueError:
                print(f"Could not convert percentage value: {percentage}")
        if data:
            return data
    return []


def parse_stock_performance(page_html):
    """Return the percent return from a StatMuse single-stock answer page, or None."""
    soup = BeautifulSoup(page_html, 'html.parser')
    for h1 in soup.find_all('h1'):
        match = re.search(r'return(?:ed|ing)\s+(-?[\d,]+(?:\.\d+)?)\s*%', h1.get_text(' ', strip=True))
        if match:
            return float(match.group(1).replace(',', ''))
    return None


def fetch_ranking(kind, year):
    """Fetch the 'best' or 'worst' performing S&P 500 stocks of a year (StatMuse lists 25)."""
    url = f"https://www.statmuse.com/money/ask/{kind}-performing-stocks-in-the-s-and-p-500-in-the-year-{year}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data from {url}")
        return []
    data = parse_ranking_table(response.text)
    if not data:
        print(f"Ranking table not found at {url}")
    return data


def get_top_n_performers(year, n):
    data = load_cache(year)
    if data:
        print(f"Using cached data for year {year}")
    else:
        data = fetch_ranking('best', year)
        if data:
            save_cache(data, year)
    # Best first
    return sorted(data, key=lambda x: x[2], reverse=True)[:n]

def get_top_n_tickers(year, n):
    top_performers = get_top_n_performers(year, n)
    return [performer[0].split('(')[-1].strip(')') for performer in top_performers]

def get_bottom_n_performers(year, n):
    data = load_cache(str(year)+"w")
    if data:
        print(f"Using cached data for year {year}")
    else:
        data = fetch_ranking('worst', year)
        if data:
            save_cache(data, str(year)+"w")
    # Worst first, so the first n really are the n worst performers
    return sorted(data, key=lambda x: x[2])[:n]

def get_bottom_n_tickers(year, n):
    bottom_performers = get_bottom_n_performers(year, n)
    return [performer[0].split('(')[-1].strip(')') for performer in bottom_performers]

def get_stock_performance(stock_symbol, year):
    # Check if we have cached data
    cached_data = load_cache(year, stock_symbol)
    if cached_data:
        print(f"Using cached data for {stock_symbol} in year {year}")
        return cached_data

    # URL of the StatMuse page for specific stock performance
    url = f"https://www.statmuse.com/money/ask/{stock_symbol}-performance-in-{year}"

    # Fetch the page content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data from {url}")
        return None

    performance_percentage = parse_stock_performance(response.text)
    if performance_percentage is None:
        print(f"Performance data not found at {url}")
        return None

    # Save the fetched data to cache
    save_cache(performance_percentage, year, stock_symbol)

    return performance_percentage

def main():
    # TODO: We could turn this into a proper CLI tool
    print("Choose an option:")
    print("1. Get top N performers of the S&P 500")
    print("2. Get bottom N performers of the S&P 500")
    print("3. Get stock performance for a specific year")
    choice = int(input("Enter your choice: "))

    if choice <= 2:
        year = int(input("Enter the calendar year: "))
        n = int(input("Enter the number of stocks to return: "))
        if choice == 1:
            top_performers = get_top_n_performers(year, n)
            print(f"Top {n} performing stocks in S&P 500 for the year {year}:")
            for performer in top_performers:
                print(f"{performer[0]}: {performer[2]:.2f}% in {performer[1]}")
        else:
            bottom_performers = get_bottom_n_performers(year, n)
            print(f"Bottom {n} performing stocks in S&P 500 for the year {year}:")
            for performer in bottom_performers:
                print(f"{performer[0]}: {performer[2]:.2f}% in {performer[1]}")
    elif choice == 3:
        stock_symbol = input("Enter the stock symbol: ").lower()
        year = int(input("Enter the calendar year: "))
        performance = get_stock_performance(stock_symbol, year)
        if performance is not None:
            print(f"{stock_symbol.upper()} returned {performance:.2f}% in {year}")

if __name__ == "__main__":
    main()
