import os
import unittest

import Parser

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "timetable_sample.html")


class TestParser(unittest.TestCase):
    def setUp(self):
        with open(FIXTURE_PATH, "rb") as f:
            self.durations, self.days = Parser.lessons(f.read())

    def test_durations_include_first_period(self):
        self.assertEqual(["07:10 - 7:55", "08:00 - 8:45"], self.durations)

    def test_plain_lesson(self):
        self.assertEqual([("MAT", "T. Testič")], self.days[0][0])

    def test_empty_slot(self):
        self.assertEqual([], self.days[1][0])

    def test_substitution_lesson(self):
        self.assertEqual([("SLJ (N)", "A. Anonim")], self.days[0][1])

    def test_employment_lesson(self):
        self.assertEqual([("ŠVZ (Z)", "M. Vzorec")], self.days[1][1])


if __name__ == "__main__":
    unittest.main()
