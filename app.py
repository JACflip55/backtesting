import datetime

import streamlit as st

import backtesting

LATEST_YEAR = datetime.date.today().year - 1  # last complete calendar year


def main():
    st.title("Stock Trading Strategy Backtester")

    start_year = st.slider('Start Year', 1980, LATEST_YEAR, 2001)
    end_year = st.slider('End Year', start_year, LATEST_YEAR, max(start_year, 2020))
    portfolio_size = st.slider('Portfolio Size', 1, 25, 15)

    top_performers = st.radio('Select performers type', ('Top Performers', 'Worst Performers')) == 'Top Performers'
    worst = not top_performers

    if st.button('Run Backtest'):
        avg_annual_return, total_return, multiplier, sorted_holdings = backtesting.calculate_strategy_return(
            start_year, end_year, portfolio_size, verbose=True, worst=worst)
        backtesting.save_cached_returns()

        # Display results
        st.write(f"Average annual return: {100*avg_annual_return:.2f}%")
        st.write(f"Total Return: ${total_return:.2f}")
        st.write(f"Return Multiplier: {multiplier:.2f}")

        # Display ordered final holdings
        st.write("Ordered Final Holdings:")
        for stock, value in sorted_holdings:
            st.write(f"{stock}: ${value:.2f}")


if __name__ == '__main__':
    main()
