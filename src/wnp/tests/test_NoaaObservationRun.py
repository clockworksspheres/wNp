# tests/test_lib.NoaaObservationRun.py

import json
import sys
import unittest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path

# Get the parent directory of the current file's parent directory
#  and add it to sys.path
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

from lib.NoaaObservationRun import NoaaObservationRun

from fixtures.noaa_observations import (
    VALID_OBSERVATION,
    CELSIUS_OBSERVATION,
    MISSING_VALUES_OBSERVATION,
    MULTI_OBSERVATION_LIST
)


class TestNoaaObservationRun(unittest.TestCase):

    @patch("noaa_sdk.NOAA.get_observations")
    def test_singleshot(self, mock_get_obs):
        mock_get_obs.return_value = iter([VALID_OBSERVATION])

        job = NoaaObservationRun()
        result = job.singleshot("83402")

        self.assertEqual(result["temperature"], 50)
        self.assertEqual(result["dewpoint"], 40)
        self.assertEqual(result["relativeHumidity"], 55)
        self.assertEqual(result["barometricPressure"], 100000)
        self.assertEqual(result["timestamp"], "530")  # 10:30 UTC → 5:30 local

    @patch("noaa_sdk.NOAA.get_observations")
    def test_singleshot_raw(self, mock_get_obs):
        mock_get_obs.return_value = iter([VALID_OBSERVATION])

        job = NoaaObservationRun()
        result = job.singleshotRaw("83402")

        self.assertEqual(result, VALID_OBSERVATION)

    @patch("lib.NoaaObservationRun.DEFAULT_DEGREES_UNITS", "C")
    @patch("noaa_sdk.NOAA.get_observations")
    def test_fordays_temperature_conversion(self, mock_get_obs):
        mock_get_obs.return_value = iter([VALID_OBSERVATION])

        job = NoaaObservationRun()
        result = job.fordays("83402", samples=1)

        expected_c = (50 - 32) * 5/9
        self.assertAlmostEqual(result[1]["temperature"], expected_c)

    @patch("lib.NoaaObservationRun.DEFAULT_DEGREES_UNITS", "F")
    @patch("noaa_sdk.NOAA.get_observations")
    def test_fordays_celsius_to_fahrenheit(self, mock_get_obs):
        mock_get_obs.return_value = iter([CELSIUS_OBSERVATION])

        job = NoaaObservationRun()
        result = job.fordays("83402", samples=1)

        expected_f = 10 * 9/5 + 32
        self.assertAlmostEqual(result[1]["temperature"], expected_f)

    @patch("noaa_sdk.NOAA.get_observations")
    def test_fordays_missing_values(self, mock_get_obs):
        mock_get_obs.return_value = iter([MISSING_VALUES_OBSERVATION])

        job = NoaaObservationRun()
        result = job.fordays("83402", samples=1)

        self.assertEqual(result[1]["temperature"], 0)
        self.assertEqual(result[1]["dewpoint"], 0)
        self.assertEqual(result[1]["relativeHumidity"], 0)
        self.assertEqual(result[1]["barometricPressure"], 0)

    @patch("noaa_sdk.NOAA.get_observations")
    def test_fordays_multiple_observations(self, mock_get_obs):
        mock_get_obs.return_value = iter(MULTI_OBSERVATION_LIST)

        job = NoaaObservationRun()
        result = job.fordays("83402", samples=3)

        self.assertEqual(len(result), 3)
        self.assertIn("temperature", result[1])
        self.assertIn("temperature", result[2])
        self.assertIn("temperature", result[3])

    @patch("noaa_sdk.NOAA.get_observations")
    def test_cache(self, mock_get_obs):
        mock_get_obs.return_value = iter([VALID_OBSERVATION])

        job = NoaaObservationRun()
        job.singleshot("83402")
        job.singleshot("83402")  # should use cache

        mock_get_obs.assert_called_once()

    @patch("builtins.open", new_callable=mock_open)
    @patch("noaa_sdk.NOAA.get_observations")
    def test_save_oneshot(self, mock_get_obs, mock_file):
        mock_get_obs.return_value = iter([VALID_OBSERVATION])

        job = NoaaObservationRun()
        job.setFileName("test.json")
        job.getAndSaveSingleShot("83402")

        mock_file.assert_called_with("test.json", "w")

    @patch("builtins.open", new_callable=mock_open)
    @patch("noaa_sdk.NOAA.get_observations")
    def test_save_raw(self, mock_get_obs, mock_file):
        mock_get_obs.return_value = iter([VALID_OBSERVATION])

        job = NoaaObservationRun()
        job.setFileName("raw.json")
        job.getAndSaveSingleShotRaw("83402")

        mock_file.assert_called_with("raw.json", "w")

