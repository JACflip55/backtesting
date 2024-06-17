import requests
from bs4 import BeautifulSoup

def get_top_n_performers(year, n):
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

    # Get the top N performers
    top_n = data[:n]

    return top_n

def main():
    year = int(input("Enter the calendar year: "))
    top_n = int(input("Enter the number of top performing stocks to return: "))

    top_performers = get_top_n_performers(year, top_n)

    # Display the top performers
    print(f"Top {top_n} performing stocks in S&P 500 for the year {year}:")
    for performer in top_performers:
        print(f"{performer[0]}: {performer[2]:.2f}% in {performer[1]}")

if __name__ == "__main__":
    main()