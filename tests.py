"""
Unit and integration tests for API Scheduler - updated for clean logger format.
Run with: python tests.py
"""

import datetime as dt
import unittest
from unittest.mock import patch, MagicMock
import main
import config

class TestScheduler(unittest.TestCase):

    def test_formatting_time_valid(self):
        """Test config.Formatting_Time parses correctly."""
        result = config.Formatting_Time("13:45:09")
        self.assertEqual(result.hour, 13)
        self.assertEqual(result.minute, 45)
        self.assertEqual(result.second, 9)

    def test_formatting_time_invalid(self):
        """Test config.Formatting_Time raises on invalid input."""
        with self.assertRaises(ValueError):
            config.Formatting_Time("invalid")

    def test_grp_timestamps_groups_correctly(self):
        """Test grp_timestamps correctly groups timestamps."""
        timestamps = ["13:45:09", "13:45:09", "17:22:00"]
        groups = main.grp_timestamps(timestamps)
        self.assertEqual(len(groups), 2)
        today = dt.date.today()
        ts1 = dt.datetime.combine(today, dt.time(13, 45, 9))
        ts2 = dt.datetime.combine(today, dt.time(17, 22, 0))
        self.assertIn(ts1, groups)
        self.assertIn(ts2, groups)
        self.assertEqual(len(groups[ts1]), 2)
        self.assertEqual(len(groups[ts2]), 1)

    def test_grp_timestamps_skips_invalid(self):
        """Test that invalid timestamps are skipped in grouping."""
        timestamps = ["13:45:09", "invalid", "17:22:00"]
        groups = main.grp_timestamps(timestamps)
        self.assertEqual(len(groups), 2)
        for group in groups.values():
            for ts in group:
                self.assertNotEqual(ts, "invalid")

    @patch('main.request.urlopen')
    @patch('main.logger')
    def test_calling_ifconfig_success(self, mock_logger, mock_urlopen):
        """Test Calling_Ifconfig logs the expected success message on successful API call."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.read.return_value = b"192.168.1.1"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        today = dt.date.today()
        target_time = dt.datetime.combine(today, dt.time(13, 45, 9))

        main.Calling_Ifconfig("13:45:09", call_id=1)

        # Assert urlopen was called once
        mock_urlopen.assert_called_once()

        # Check that logger.info was called with the correct success message format
        expected_log_msg = f"{target_time.strftime('%Y-%m-%d %H:%M:%S')}: Successfully called API at ifconfig.co"
        mock_logger.info.assert_any_call(expected_log_msg)

    @patch('main.request.urlopen')
    @patch('main.logger')
    def test_calling_ifconfig_failure(self, mock_logger, mock_urlopen):
        """Test Calling_Ifconfig logs a warning on network failure."""
        mock_urlopen.side_effect = Exception("Network failure")

        main.Calling_Ifconfig("13:45:09", call_id=1)

        # Check that logger.error was called indicating error
        mock_logger.error.assert_called()

if __name__ == "__main__":
    unittest.main(verbosity=2)