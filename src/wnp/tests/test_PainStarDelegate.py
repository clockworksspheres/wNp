import sys
import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
from pathlib import Path

# Get the parent directory of the current file's parent directory
#  and add it to sys.path
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest

# Import your classes
from PainStarDelegate import PainTrackerWidget, PainTableModel


app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)


class TestPainTableModel(unittest.TestCase):

    def setUp(self):
        self.model = PainTableModel()

    def test_row_count(self):
        self.assertEqual(self.model.rowCount(), len(self.model.body_parts))

    def test_column_count(self):
        self.assertEqual(self.model.columnCount(), 2)

    def test_set_data(self):
        index = self.model.index(0, 1)
        result = self.model.setData(index, 5)

        self.assertTrue(result)
        self.assertEqual(self.model.data_list[0][1], 5)

    def test_get_all_data(self):
        data = self.model.get_all_data()
        self.assertEqual(len(data), len(self.model.body_parts))
        self.assertIn("body_part", data[0])
        self.assertIn("pain_level", data[0])


class TestPainTrackerWidget(unittest.TestCase):

    def setUp(self):
        self.widget = PainTrackerWidget()
        self.widget.show()

    def tearDown(self):
        self.widget.close()

    def test_notes_set_and_get(self):
        text = "Pain increased after walking"

        self.widget.set_notes(text)

        self.assertEqual(
            self.widget.notes_edit.toPlainText(),
            text
        )

    def test_set_ratings(self):
        ratings = {
            "Head / Migraine": 7,
            "Neck": 4
        }

        self.widget.set_ratings(ratings)

        data = self.widget.get_ratings()

        lookup = {x["body_part"]: x["pain_level"] for x in data}

        self.assertEqual(lookup["Head / Migraine"], 7)
        self.assertEqual(lookup["Neck"], 4)

    def test_clear_all(self):
        self.widget.notes_edit.setPlainText("Test")

        self.widget.model.data_list[0][1] = 5

        self.widget.clear_all()

        self.assertEqual(self.widget.notes_edit.toPlainText(), "")

        for row in self.widget.model.data_list:
            self.assertEqual(row[1], 0)

    def test_get_full_data(self):
        self.widget.notes_edit.setPlainText("Testing")

        data = self.widget.get_full_data()

        self.assertIn("assessment_datetime", data)
        self.assertEqual(data["notes"], "Testing")
        self.assertEqual(len(data["ratings"]), len(self.widget.model.body_parts))


class TestSaveRatings(unittest.TestCase):

    def setUp(self):
        self.widget = PainTrackerWidget()
        self.widget.show()

    def tearDown(self):
        self.widget.close()

    @patch("PainStarDelegate.QMessageBox")
    @patch("PainStarDelegate.QFileDialog.getSaveFileName")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_ratings_success(
        self,
        mock_file,
        mock_dialog,
        mock_msgbox
    ):
        mock_dialog.return_value = ("test.json", "json")

        self.widget.notes_edit.setPlainText("Test notes")

        self.widget.save_ratings()

        mock_file.assert_called_once()

        mock_msgbox.information.assert_called_once()

    @patch("PainStarDelegate.QMessageBox")
    @patch("PainStarDelegate.QFileDialog.getSaveFileName")
    @patch("builtins.open", side_effect=Exception("disk error"))
    def test_save_ratings_failure(
        self,
        mock_open_file,
        mock_dialog,
        mock_msgbox
    ):
        mock_dialog.return_value = ("test.json", "json")

        self.widget.save_ratings()

        mock_msgbox.critical.assert_called_once()

    @patch("PainStarDelegate.QFileDialog.getSaveFileName")
    def test_save_cancelled(self, mock_dialog):
        mock_dialog.return_value = ("", "")

        with patch.object(self.widget, "update_datetime") as mock_update:
            self.widget.save_ratings()

        mock_update.assert_called_once()


class TestGuiInteraction(unittest.TestCase):

    def setUp(self):
        self.widget = PainTrackerWidget()
        self.widget.show()

    def tearDown(self):
        self.widget.close()

    def test_button_click(self):
        with patch.object(self.widget, "save_ratings") as mock_save:
            QTest.mouseClick(
                self.widget.save_button,
                Qt.MouseButton.LeftButton
            )

            mock_save.assert_called_once()


if __name__ == "__main__":
    unittest.main()

