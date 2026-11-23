"""Cache tests: JSON round trips and pick-up of pickles written by older versions. Uses temp dirs only."""
import os
import pickle
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import backtesting  # noqa: E402
import statmuse  # noqa: E402


class CacheTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.new = os.path.join(tmp.name, "cache")
        self.legacy = os.path.join(tmp.name, "__pycache__")
        os.makedirs(self.legacy)
        for patcher in (
            mock.patch.object(statmuse, "CACHE_DIR", os.path.join(self.new, "statmuse")),
            mock.patch.object(statmuse, "LEGACY_CACHE_DIR", self.legacy),
            mock.patch.object(backtesting, "fn_cached_returns", os.path.join(self.new, "cached_returns.json")),
            mock.patch.object(backtesting, "fn_legacy_cached_returns", os.path.join(self.legacy, "cached_returns.pk")),
        ):
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_statmuse_round_trip(self):
        rows = [["Tesla (TSLA)", "2020", 731.18]]
        self.assertIsNone(statmuse.load_cache(2020))
        statmuse.save_cache(rows, 2020)
        statmuse.save_cache(80.7, 2020, "aapl")
        self.assertEqual(statmuse.load_cache(2020), rows)
        self.assertEqual(statmuse.load_cache(2020, "aapl"), 80.7)
        self.assertIsNone(statmuse.load_cache("2020w"))

    def test_statmuse_legacy_pickle_is_picked_up_and_migrated(self):
        rows = [["Carnival (CCL)", "2020", -57.33]]
        with open(os.path.join(self.legacy, "2020w.pkl"), "wb") as f:
            pickle.dump(rows, f)
        self.assertEqual(statmuse.load_cache("2020w"), rows)
        self.assertTrue(os.path.exists(os.path.join(statmuse.CACHE_DIR, "2020w.json")))

    def test_returns_round_trip_keeps_integer_years(self):
        with mock.patch.object(backtesting, "cached_returns", {2020: {"AAPL": 1.8, "ZZZ": 0}}):
            backtesting.save_cached_returns()
        self.assertEqual(backtesting.load_cached_returns(), {2020: {"AAPL": 1.8, "ZZZ": 0}})

    def test_returns_legacy_pickle_and_empty_start(self):
        self.assertEqual(backtesting.load_cached_returns(), {})
        with open(backtesting.fn_legacy_cached_returns, "wb") as f:
            pickle.dump({2001: {"AAA": 1.1}}, f)
        self.assertEqual(backtesting.load_cached_returns(), {2001: {"AAA": 1.1}})


if __name__ == "__main__":
    unittest.main()
