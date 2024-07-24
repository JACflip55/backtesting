import requests
from bs4 import BeautifulSoup
import pickle
import os

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

def get_top_n_performers(year, n):
    # Check if we have cached data
    cached_data = load_cache(year)
    if cached_data:
        print(f"Using cached data for year {year}")
        data = cached_data
    else:
        # URL of the StatMuse page for S&P 500 top performers
        url = f"https://www.statmuse.com/money/ask/best-performing-stocks-in-the-s-and-p-500-in-the-year-{year}"

        # Fetch the page content
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch data from {url}")
            return []

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table body
        tbody = soup.find('tbody', class_='divide-y divide-[#c7c8ca] leading-[22px]')
        if not tbody:
            print("Table body not found in the HTML content")
            return []

        # Extract the rows
        rows = tbody.find_all('tr')

        # Extract and store data
        data = []
        for row in rows:
            columns = row.find_all('td')
            if len(columns) < 3:
                continue
            name = columns[0].get_text(strip=True)
            year_fetched = columns[1].get_text(strip=True)
            percentage = columns[2].get_text(strip=True).replace('%', '')

            try:
                percentage_float = float(percentage)
                data.append([name, year_fetched, percentage_float])
            except ValueError:
                print(f"Could not convert percentage value: {percentage}")
                continue

        # Sort data by percentage (descending)
        data.sort(key=lambda x: x[2], reverse=True)

        # Save the fetched data to cache
        save_cache(data, year)

    # Get the top N performers
    top_n = data[:n]
    return top_n

def get_top_n_tickers(year, n):
    top_performers = get_top_n_performers(year, n)
    return [performer[0].split('(')[-1].strip(')') for performer in top_performers]

def get_bottom_n_performers(year, n):
    # Check if we have cached data
    cached_data = load_cache(str(year)+"w")
    if cached_data:
        print(f"Using cached data for year {year}")
        data = cached_data
    else:
        # URL of the StatMuse page for S&P 500 top performers
        url = f"https://www.statmuse.com/money/ask/worst-performing-stocks-in-the-s-and-p-500-in-the-year-{year}"

        # Fetch the page content
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch data from {url}")
            return []

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table body
        tbody = soup.find('tbody', class_='divide-y divide-gray-6 dark:divide-gray-4 leading-[22px]')
        if not tbody:
            print("Table body not found in the HTML content")
            return []

        # Extract the rows
        rows = tbody.find_all('tr')

        # Extract and store data
        data = []
        for row in rows:
            columns = row.find_all('td')
            if len(columns) < 3:
                continue
            name = columns[0].get_text(strip=True)
            year_fetched = columns[1].get_text(strip=True)
            percentage = columns[2].get_text(strip=True).replace('%', '')

            try:
                percentage_float = float(percentage)
                data.append([name, year_fetched, percentage_float])
            except ValueError:
                print(f"Could not convert percentage value: {percentage}")
                continue

        # Sort data by percentage (descending)
        data.sort(key=lambda x: x[2], reverse=True)

        # Save the fetched data to cache
        save_cache(data, str(year)+"w")

    # Get the top N performers
    top_n = data[:n]
    return top_n


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

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the performance element
    h1_tag = soup.find('h1', class_='font-semibold text-xl md:text-2xl md:leading-snug lg:text-[1.75rem] xl:text-3xl xl:leading-snug my-auto')
    if not h1_tag:
        print("Performance data not found in the HTML content")
        return None

    p_tag = h1_tag.find('p', class_='my-[1em] [&>a]:underline [&>a]:text-team-secondary')
    if not p_tag:
        print("Performance data not found in the paragraph")
        return None

    performance_text = p_tag.get_text(strip=True)
    percentage_str = performance_text.split('returned')[-1].split('%')[0].strip()

    try:
        performance_percentage = float(percentage_str)
    except ValueError:
        print(f"Could not convert performance value: {percentage_str}")
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
