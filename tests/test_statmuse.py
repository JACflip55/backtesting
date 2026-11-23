"""Parsing tests for the StatMuse scraper. No network: pages are inline HTML."""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import statmuse  # noqa: E402

RANKING_PAGE = """
<html><body>
<h1 class="whatever"><p>Tesla (TSLA) had the best year in 2020, returning 731.2%.</p></h1>
<table><thead><tr><th>ASSET</th><th>YEAR</th><th>% RETURN</th></tr></thead>
<tbody class="some-class that-changes">
<tr><td><a>Moderna (MRNA)</a></td><td>2020</td><td>433.83%</td></tr>
<tr><td><a>Tesla (TSLA)</a></td><td>2020</td><td>731.18%</td></tr>
<tr><td><a>Carnival (CCL)</a></td><td>2020</td><td>-57.33%</td></tr>
<tr><td>Big (BIG)</td><td>2020</td><td>1,234.5%</td></tr>
<tr><td colspan="2">not a data row</td></tr>
</tbody></table>
</body></html>
"""
ROWS = [["Moderna (MRNA)", "2020", 433.83], ["Tesla (TSLA)", "2020", 731.18],
        ["Carnival (CCL)", "2020", -57.33], ["Big (BIG)", "2020", 1234.5]]


class ParsingTest(unittest.TestCase):
    def test_ranking_table_is_found_whatever_its_css_class(self):
        self.assertEqual(statmuse.parse_ranking_table(RANKING_PAGE), ROWS)

    def test_page_without_a_table(self):
        self.assertEqual(statmuse.parse_ranking_table("<html><body><h1>Nothing</h1></body></html>"), [])

    def test_stock_performance(self):
        page = '<h1 class="x"><p>Apple ( <a>AAPL</a> ) returned 80.7% in 2020.</p></h1>'
        self.assertEqual(statmuse.parse_stock_performance(page), 80.7)
        self.assertEqual(statmuse.parse_stock_performance("<h1><p>X (X) returned -12.5% in 2008.</p></h1>"), -12.5)
        self.assertIsNone(statmuse.parse_stock_performance("<h1>No answer</h1>"))


class SignInWallTest(unittest.TestCase):
    WALL_PAGE = "<html><body><h1><p>Carvana (CVNA) had the best year in 2019, returning 190.6%.</p></h1>" \
                "<div>Keep musing with a free StatMuse account</div></body></html>"

    def fetch(self, page):
        response = mock.Mock(status_code=200, text=page)
        with mock.patch.object(statmuse.requests, "get", return_value=response), \
                mock.patch.object(statmuse, "load_cache", return_value=None), \
                mock.patch.object(statmuse, "save_cache") as save:
            try:
                return statmuse.get_top_n_tickers(2019, 5), save
            except statmuse.StatMuseLimitReached:
                return "limit", save

    def test_withheld_table_raises_instead_of_returning_no_stocks(self):
        result, save = self.fetch(self.WALL_PAGE)
        self.assertEqual(result, "limit")
        save.assert_not_called()

    def test_normal_page_is_parsed_and_cached(self):
        result, save = self.fetch(RANKING_PAGE)
        self.assertEqual(result, ["BIG", "TSLA", "MRNA", "CCL"])
        save.assert_called_once()


class SelectionTest(unittest.TestCase):
    def setUp(self):
        for patcher in (
            mock.patch.object(statmuse, "load_cache", lambda *a, **k: [list(r) for r in ROWS]),
            mock.patch.object(statmuse.requests, "get", side_effect=AssertionError("network call in a unit test")),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_top_n_are_the_best(self):
        self.assertEqual(statmuse.get_top_n_tickers(2020, 2), ["BIG", "TSLA"])

    def test_bottom_n_are_the_worst(self):
        self.assertEqual(statmuse.get_bottom_n_tickers(2020, 2), ["CCL", "MRNA"])


if __name__ == "__main__":
    unittest.main()
