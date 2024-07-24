import streamlit as st
import backtesting_experiment as be

def main():
    st.title("Stock Trading Strategy Backtester")

    start_year = st.slider('Start Year', 1980, 2023, 2001)
    end_year = st.slider('End Year', start_year, 2023, 2020)
    portfolio_size = st.slider('Portfolio Size', 1, 25, 15)

    top_performers = st.radio('Select performers type', ('Top Performers', 'Worst Performers')) == 'Top Performers'
    worst = not top_performers

    if st.button('Run Backtest'):
        avg_apr, total_return, multiplier = be.calculate_strategy_return(start_year, end_year, portfolio_size, verbose=False, worst=worst)

        # Display results
        st.write(f"Average APR: %{100*avg_apr:.2f}")
        st.write(f"Total Return: ${total_return:.2f}")
        st.write(f"Return Multiplier: {multiplier:.2f}")

        # Display ordered final holdings
        stock_holdings = be.calculate_strategy_return(start_year, end_year, portfolio_size, verbose=True, worst=worst)[3]
        sorted_holdings = sorted(stock_holdings.items(), key=lambda x: x[1], reverse=True)
        st.write("Ordered Final Holdings:")
        for stock, value in sorted_holdings:
            st.write(f"{stock}: ${value:.2f}")

if __name__ == '__main__':
    main()