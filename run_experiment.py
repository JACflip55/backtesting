import backtesting

## Experiment configuration
length_of_experiment = 15 # Number of years to run the experiment for
earliest_year_in_data = 1980  # Cannot get earlier data than 1962 from statmuse
portfolio_compositions = [10, 15, 20, 25]  # Cannot get more than 25 from statmuse

def run_experiment():
    ## Do Setup
    portfolio_results = {n: {'top': [], 'bottom': []} for n in portfolio_compositions}
    portfolio_percent_return_results = {n: {'top': [], 'bottom': []} for n in portfolio_compositions}
    best_portfolio_counts = {n: 0 for n in portfolio_compositions}
    worst_portfolio_counts = {n: 0 for n in portfolio_compositions}
    baseline_results = []
    periods = [(start, start + length_of_experiment - 1) for start in range(earliest_year_in_data, 2024 - length_of_experiment)]
    results = []

    for starty, endy in periods:
        print(f"Running experiment for {starty}-{endy}...")
        period_results = []

        for n in portfolio_compositions:
            avg_annual_return_n, return_n, multiplier_n = backtesting.calculate_strategy_return(starty, endy, n)
            portfolio_results[n]['top'].append(multiplier_n)
            portfolio_percent_return_results[n]['top'].append(avg_annual_return_n)
            period_results.append((avg_annual_return_n, return_n, multiplier_n, f'Top {n} stocks'))

            avg_annual_return_n_worst, return_n_worst, multiplier_n_worst = backtesting.calculate_strategy_return(starty, endy, n, worst=True)
            portfolio_results[n]['bottom'].append(multiplier_n_worst)
            portfolio_percent_return_results[n]['bottom'].append(avg_annual_return_n_worst)
            period_results.append((avg_annual_return_n_worst, return_n_worst, multiplier_n_worst, f'Bottom {n} stocks'))

        baseline_apr, baseline_return, baseline_multiplier = backtesting.baseline_test("^GSPC", starty, endy)
        baseline_results.append(baseline_multiplier)
        period_results.append((baseline_apr, baseline_return, baseline_multiplier, 'S&P 500 baseline'))

        best_portfolio = max(period_results, key=lambda x: x[1])
        if 'Top' in best_portfolio[3]:
            best_n = int(best_portfolio[3].split()[1])
            best_portfolio_counts[best_n] += 1
        elif 'Bottom' in best_portfolio[3]:
            worst_n = int(best_portfolio[3].split()[1])
            worst_portfolio_counts[worst_n] += 1

        results.append((starty, endy, period_results))

    print_experiment_results(results, portfolio_compositions, portfolio_results, best_portfolio_counts, worst_portfolio_counts, baseline_results, baseline_apr, portfolio_percent_return_results)

def print_experiment_results(results, portfolio_compositions, portfolio_results, best_portfolio_counts, worst_portfolio_counts, baseline_results, baseline_apr, portfolio_percent_return_results):
    print("\n\n\n")
    print("Experiment Results:\n")

    for result in results:
        starty, endy, period_results = result
        print(f"Period: {starty}-{endy}")
        for apr, return_val, multiplier, description in period_results:
            print(f"{description} return: ${return_val:.2f}, Multiplier: {multiplier:.2f}, APR: %{100 * apr:.2f}")
        best_portfolio = max(period_results, key=lambda x: x[1])
        print(f"Best performing portfolio: {best_portfolio[3]} with return: %{100 * best_portfolio[0]:.2f}")
        print("\n")

    print("\n\nSummary:\n")
    for n in portfolio_compositions:
        avg_multiplier_top = sum(portfolio_results[n]['top']) / len(portfolio_results[n]['top'])
        avg_multiplier_bottom = sum(portfolio_results[n]['bottom']) / len(portfolio_results[n]['bottom'])
        print(f"Top {n} stocks average multiplier: {avg_multiplier_top:.2f}")
        print(f"Top {n} stocks were the best performer in {best_portfolio_counts[n]} periods")
        avg_apr_top = sum(portfolio_percent_return_results[n]['top']) / len(portfolio_percent_return_results[n]['top'])
        print(f"Top {n} stocks average APR: %{100 * avg_apr_top:.2f}")

        print(f"Bottom {n} stocks average multiplier: {avg_multiplier_bottom:.2f}")
        print(f"Bottom {n} stocks were the best performer in {worst_portfolio_counts[n]} periods")
        avg_apr_bottom = sum(portfolio_percent_return_results[n]['bottom']) / len(portfolio_percent_return_results[n]['bottom'])
        print(f"Bottom {n} stocks average APR: %{100 * avg_apr_bottom:.2f}")

    avg_baseline_multiplier = sum(baseline_results) / len(baseline_results)
    print(f"S&P 500 baseline average multiplier: {avg_baseline_multiplier:.2f}")
    print(f"S&P 500 baseline was the best performer in {len(results) - sum(best_portfolio_counts.values()) - sum(worst_portfolio_counts.values())} periods")
    print(f"S&P 500 baseline average APR: %{100 * baseline_apr:.2f}")


def print_compound_interest_comparisons():
    print("\n\n\n")
    print("Compound Interest Comparisons for {length_of_experiment} years:\n")
    for i in range(12, 50):
        percentage = 0.005 * i  # increment by 1/2 percent
        print(f"Compound interest at {percentage*100:.2f}% per year:")
        return_15, multiplier_15 = compound_interest_calculator(percentage, length_of_experiment)
        print(f"Return: ${return_15:.2f}, Multiplier: {multiplier_15:.2f}")
        print("\n")

# Run the experiment
run_experiment()
# print_compound_interest_comparisons()
## Can use this to quickly get an idea for the avg interest rate
