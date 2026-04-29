import sys
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Get the parent directory of the current file's parent directory
#  and add it to sys.path
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt

import wnp


# Ensure single QApplication instance
app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)


class TestGraphWindow(unittest.TestCase):

    def test_graph_window_creation(self):
        x = [1,2,3]
        y = [4,5,6]

        window = wnp.GraphWindow(
            "Test Graph",
            x,
            y,
            "Time",
            "Temp"
        )

        self.assertEqual(window.windowTitle(), "Test Graph")
        self.assertIsNotNone(window.plot_widget)


class TestMainWindow(unittest.TestCase):

    def setUp(self):
        self.window = wnp.MainWindow()
        self.window.show()

    def tearDown(self):
        self.window.close()

    def test_default_zip_country(self):

        self.assertEqual(
            self.window.zipLineEdit.text(),
            "83402"
        )

        self.assertEqual(
            self.window.countryLineEdit.text(),
            "US"
        )

    @patch("wnp.NoaaObservationRun")
    def test_get_live_observations(self, mock_noaa):

        fake_instance = MagicMock()

        fake_instance.fordays.return_value = {
            "1": {"temperature": 10},
            "2": {"temperature": 20},
            "3": {"temperature": 30},
        }

        self.window.njob = fake_instance

        wtime, data = self.window.get_live_observations("temperature")

        self.assertEqual(len(data), 3)
        self.assertEqual(len(wtime), 3)

    @patch("wnp.GraphWindow")
    def test_show_graph1(self, mock_graph):

        mock_graph_instance = MagicMock()
        mock_graph.return_value = mock_graph_instance

        with patch.object(
            self.window,
            "get_live_observations",
            return_value=([1,2,3],[10,20,30])
        ):
            self.window.show_graph1()

        mock_graph.assert_called_once()
        mock_graph_instance.show.assert_called_once()

    @patch("wnp.GraphWindow")
    def test_show_graph_all(self, mock_graph):

        mock_graph_instance = MagicMock()
        mock_graph.return_value = mock_graph_instance

        with patch.object(
            self.window,
            "get_live_observations",
            return_value=([1,2,3],[10,20,30])
        ):
            self.window.show_graphAll()

        self.assertEqual(mock_graph.call_count, 4)
        self.assertEqual(mock_graph_instance.show.call_count, 4)

    @patch("wnp.PainTrackerWidget")
    def test_pain_survey(self, mock_pain):

        mock_widget = MagicMock()
        mock_pain.return_value = mock_widget

        self.window.pain_survey()

        mock_pain.assert_called_once()
        mock_widget.show.assert_called_once()


class TestGUIButtons(unittest.TestCase):

    def setUp(self):
        self.window = wnp.MainWindow()
        self.window.show()

    def tearDown(self):
        self.window.close()

    def _get_button(self, text):
        for widget in self.window.findChildren(type(self.window.findChild(type(self.window.zipLineEdit)))):
            pass

    @patch.object(wnp.MainWindow, "show_graph1")
    def test_temperature_button(self, mock_func):

        buttons = self.window.findChildren(wnp.QPushButton)

        for b in buttons:
            if b.text() == "Temperature":
                QTest.mouseClick(b, Qt.LeftButton)

        mock_func.assert_called_once()

    @patch.object(wnp.MainWindow, "show_graph2")
    def test_humidity_button(self, mock_func):

        buttons = self.window.findChildren(wnp.QPushButton)

        for b in buttons:
            if b.text() == "Relative Humidity":
                QTest.mouseClick(b, Qt.LeftButton)

        mock_func.assert_called_once()

    @patch.object(wnp.MainWindow, "pain_survey")
    def test_pain_survey_button(self, mock_func):

        buttons = self.window.findChildren(wnp.QPushButton)

        for b in buttons:
            if b.text() == "Pain Survey":
                QTest.mouseClick(b, Qt.LeftButton)

        mock_func.assert_called_once()


if __name__ == "__main__":
    unittest.main()

