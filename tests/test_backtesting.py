"""Unit tests for the strategy maths. No network: stock picks and yearly returns are stubbed."""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import backtesting  # noqa: E402

# year -> {ticker: price multiplier for that year}
RETURNS = {
    2001: {"AAA": 1.10, "BBB": 0.90},
    2002: {"AAA": 1.20, "BBB": 1.00, "CCC": 2.00},
}
PICKS = {2000: ["AAA", "BBB"], 2001: ["AAA", "CCC"]}  # picks are made from the previous year's ranking


class StrategyTest(unittest.TestCase):
    def setUp(self):
        for patcher in (
            mock.patch.object(backtesting, "cached_returns", {y: dict(r) for y, r in RETURNS.items()}),
            mock.patch.object(backtesting, "annual_investment_total", 20000),
            mock.patch.object(backtesting.statmuse, "get_top_n_tickers", lambda year, n: PICKS[year][:n]),
            mock.patch.object(backtesting.statmuse, "get_bottom_n_tickers", lambda year, n: PICKS[year][::-1][:n]),
            mock.patch.object(backtesting.yf, "download", side_effect=AssertionError("network call in a unit test")),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_two_year_strategy(self):
        avg, total_return, multiplier = backtesting.calculate_strategy_return(2001, 2002, 2)
        # 2001: 10000 each in AAA, BBB -> 11000 + 9000 = 20000 (0% on 20000)
        # 2002: +10000 AAA, +10000 CCC -> AAA 21000*1.2, BBB 9000*1.0, CCC 10000*2.0 = 54200 (35.5% on 40000)
        self.assertAlmostEqual(total_return, 54200 - 40000)
        self.assertAlmostEqual(multiplier, 54200 / 40000)
        self.assertAlmostEqual(avg, (0.0 + 0.355) / 2)

    def test_verbose_returns_holdings_largest_first(self):
        *_, holdings = backtesting.calculate_strategy_return(2001, 2002, 2, verbose=True)
        self.assertEqual([ticker for ticker, _ in holdings], ["AAA", "CCC", "BBB"])
        self.assertAlmostEqual(dict(holdings)["AAA"], 25200)

    def test_worst_performers_use_bottom_ranking(self):
        _, _, multiplier = backtesting.calculate_strategy_return(2001, 2001, 1, worst=True)
        self.assertAlmostEqual(multiplier, 0.90)  # all 20000 in BBB

    def test_worthless_stock_is_dropped(self):
        backtesting.cached_returns[2001]["BBB"] = 0
        portfolio = backtesting.update_portfolio({"AAA": 100.0, "BBB": 100.0}, 2001)
        self.assertEqual(list(portfolio), ["AAA"])
        self.assertAlmostEqual(portfolio["AAA"], 110.0)

    def test_baseline(self):
        avg, total_return, multiplier = backtesting.baseline_test("AAA", 2001, 2002)
        # 20000*1.1 = 22000; (22000 + 20000)*1.2 = 50400
        self.assertAlmostEqual(total_return, 50400 - 40000)
        self.assertAlmostEqual(multiplier, 1.26)
        self.assertAlmostEqual(avg, (0.10 + 0.20) / 2)

    def test_compound_interest(self):
        total_return, multiplier = backtesting.compound_interest_calculator(0.10, 2)
        self.assertAlmostEqual(total_return, 46200 - 40000)
        self.assertAlmostEqual(multiplier, 1.155)


if __name__ == "__main__":
    unittest.main()
