import unittest
from flask import url_for, request
from datetime import datetime, timedelta

def daterange(start_date, end_date):  
    # https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def clean_data(start_date, end_date, data):
                date = []
                severity = []
                severity_dict = {
                    "Not at all": 0,
                    "A little bit": 1,
                    "Somewhat": 2,
                    "Quite a bit": 3,
                    "Very much": 4,
                }
                r = {}
                for row in data:
                    row = row["row"][1:-1].split(",")
                    if row[0] in r:
                        r[row[0]] += [[row[1].strip('"'), row[2].strip('"')]]
                    else:
                        r[row[0]] = [[row[1].strip('"'), row[2].strip('"')]]

                for single_date in daterange(start_date, end_date + timedelta(1)):

                    d = single_date.strftime("%Y-%m-%d")
                    date += [d + " "]
                    date += [d + ""]
                    date += [d + "\n"]
                    if d in r:
                        if len(r[d]) == 3:
                            severity += [
                                {"value": severity_dict[r[d][0][0]], "label": "Morning"}
                            ]
                            severity += [
                                {"value": severity_dict[r[d][1][0]], "label": "Daytime"}
                            ]
                            severity += [
                                {"value": severity_dict[r[d][2][0]], "label": "Night-time"}
                            ]

                        elif len(r[d]) == 2:
                            if r[d][0][1] == "Morning" and r[d][1][1] == "Daytime":
                                severity += [
                                    {"value": severity_dict[r[d][0][0]], "label": "Morning"}
                                ]
                                severity += [
                                    {"value": severity_dict[r[d][1][0]], "label": "Daytime"}
                                ]
                                severity += [None]
                            elif r[d][0][1] == "Morning" and r[d][1][1] == "Night-time":
                                severity += [
                                    {"value": severity_dict[r[d][0][0]], "label": "Morning"}
                                ]
                                severity += [None]
                                severity += [
                                    {
                                        "value": severity_dict[r[d][1][0]],
                                        "label": "Night-time",
                                    }
                                ]
                            else:
                                severity += [None]
                                severity += [
                                    {"value": severity_dict[r[d][0][0]], "label": "Daytime"}
                                ]
                                severity += [
                                    {
                                        "value": severity_dict[r[d][1][0]],
                                        "label": "Night-time",
                                    }
                                ]
                        else:
                            if r[d][0][1] == "All the time":
                                severity += [
                                    {"value": severity_dict[r[d][0][0]], "label": "Morning"}
                                ]
                                severity += [
                                    {"value": severity_dict[r[d][0][0]], "label": "Daytime"}
                                ]
                                severity += [
                                    {
                                        "value": severity_dict[r[d][0][0]],
                                        "label": "Night-time",
                                    }
                                ]
                            elif r[d][0][1] == "Sporadic":
                                severity += [
                                    {
                                        "value": severity_dict[r[d][0][0]],
                                        "label": "Sporadic",
                                    }
                                ] * 3
                            elif r[d][0][1] == "Morning":
                                severity += [
                                    {"value": severity_dict[r[d][0][0]], "label": "Morning"}
                                ]
                                severity += [None]
                                severity += [None]
                            elif r[d][0][1] == "Daytime":
                                severity += [None]
                                severity += [
                                    {"value": severity_dict[r[d][0][0]], "label": "Daytime"}
                                ]
                                severity += [None]
                            else:
                                severity += [None]
                                severity += [None]
                                severity += [
                                    {
                                        "value": severity_dict[r[d][0][0]],
                                        "label": "Night-time",
                                    }
                                ]

                    else:
                        severity += [None] * 3

                return date, severity

class CleanDateTests(unittest.TestCase):
    def test_all_the_time(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 30)
        data = [{'row': '(2020-08-30,Quite a bit,All the time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, {"value": 3, "label": "Night-time"}])

    def test_sporadic(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 30)
        data = [{'row': '(2020-08-30,Quite a bit,Sporadic,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Sporadic"}, 
            {"value": 3, "label": "Sporadic"}, {"value": 3, "label": "Sporadic"}])

    def test_morn_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 30)
        data = [{'row': '(2020-08-30,Not at all,Morning,"")'}, {'row': '(2020-08-30,Quite a bit,Daytime,"")'},
            {'row': '(2020-08-30,Somewhat,Nigh-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n"])
        self.assertEqual(severity, [{"value": 0, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, {"value": 2, "label": "Night-time"}])

    def test_morn_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 30)
        data = [{'row': '(2020-08-30,Not at all,Morning,"")'}, {'row': '(2020-08-30,Quite a bit,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n"])
        self.assertEqual(severity, [{"value": 0, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, None])

    def test_morn_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 30)
        data = [{'row': '(2020-08-30,Not at all,Morning,"")'}, {'row': '(2020-08-30,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n"])
        self.assertEqual(severity, [{"value": 0, "label": "Morning"}, None, {"value": 3, "label": "Night-time"}])

    def test_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 30)
        data = [{'row': '(2020-08-30,Not at all,Daytime,"")'}, {'row': '(2020-08-30,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n"])
        self.assertEqual(severity, [None, {"value": 0, "label": "Daytime"},
            {"value": 3, "label": "Night-time"}])

    def test_morn(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 30)
        data = [{'row': '(2020-08-30,Not at all,Morning,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n"])
        self.assertEqual(severity, [{"value": 0, "label": "Morning"}, None, None])

    def test_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 30)
        data = [{'row': '(2020-08-30,Not at all,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n"])
        self.assertEqual(severity, [None, {"value": 0, "label": "Daytime"}, None])

    def test_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 30)
        data = [{'row': '(2020-08-30,Not at all,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n"])
        self.assertEqual(severity, [None, None, {"value": 0, "label": "Night-time"}])

    def test_all_the_time_all_the_time(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Quite a bit,All the time,"")'}, {'row': '(2020-08-31,A little bit,All the time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, {"value": 3, "label": "Night-time"}, {"value": 1, "label": "Morning"}, 
            {"value": 1, "label": "Daytime"}, {"value": 1, "label": "Night-time"}])

    def test_all_the_time_sporadic(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Quite a bit,All the time,"")'}, {'row': '(2020-08-31,A little bit,Sporadic,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, {"value": 3, "label": "Night-time"}, {"value": 1, "label": "Sporadic"}, 
            {"value": 1, "label": "Sporadic"}, {"value": 1, "label": "Sporadic"}])

    def test_all_the_time_morn_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Quite a bit,All the time,"")'}, {'row': '(2020-08-31,A little bit,Morning,"")'}, 
            {'row': '(2020-08-31,Very much,Daytime,"")'}, {'row': '(2020-08-31,Somewhat,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, {"value": 3, "label": "Night-time"}, {"value": 1, "label": "Morning"}, 
            {"value": 4, "label": "Daytime"}, {"value": 2, "label": "Night-time"}])

    def test_all_the_time_morn_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Quite a bit,All the time,"")'}, {'row': '(2020-08-31,Not at all,Morning,"")'},
            {'row': '(2020-08-31,Quite a bit,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, {"value": 3, "label": "Night-time"}, {"value": 0, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, None])

    def test_all_the_time_morn_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Quite a bit,All the time,"")'}, {'row': '(2020-08-31,Not at all,Morning,"")'},
            {'row': '(2020-08-31,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, {"value": 3, "label": "Night-time"}, {"value": 0, "label": "Morning"},
            None, {"value": 3, "label": "Night-time"}])

    def test_all_the_time_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Quite a bit,All the time,"")'}, {'row': '(2020-08-31,Not at all,Daytime,"")'}, 
        {'row': '(2020-08-31,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Morning"}, {"value": 3, "label": "Daytime"}, 
            {"value": 3, "label": "Night-time"}, None, {"value": 0, "label": "Daytime"},
            {"value": 3, "label": "Night-time"}])

    def test_all_the_time_morn(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Quite a bit,All the time,"")'}, {'row': '(2020-08-31,Not at all,Morning,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Morning"}, {"value": 3, "label": "Daytime"}, 
            {"value": 3, "label": "Night-time"}, {"value": 0, "label": "Morning"}, None, None])

    def test_all_the_time_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Quite a bit,All the time,"")'}, {'row': '(2020-08-31,Not at all,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Morning"}, {"value": 3, "label": "Daytime"}, 
            {"value": 3, "label": "Night-time"}, None, {"value": 0, "label": "Daytime"}, None])

    def test_all_the_time_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Quite a bit,All the time,"")'}, {'row': '(2020-08-31,Not at all,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Morning"}, {"value": 3, "label": "Daytime"}, 
            {"value": 3, "label": "Night-time"}, None, None, {"value": 0, "label": "Night-time"}])
    
    def test_sporadic_all_the_time(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Quite a bit,Sporadic,"")'}, {'row': '(2020-08-31,A little bit,All the time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Sporadic"}, 
            {"value": 3, "label": "Sporadic"}, {"value": 3, "label": "Sporadic"}, {"value": 1, "label": "Morning"}, 
            {"value": 1, "label": "Daytime"}, {"value": 1, "label": "Night-time"}])

    def test_sporadic_sporadic(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Quite a bit,Sporadic,"")'}, {'row': '(2020-08-31,A little bit,Sporadic,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Sporadic"}, 
            {"value": 3, "label": "Sporadic"}, {"value": 3, "label": "Sporadic"}, {"value": 1, "label": "Sporadic"}, 
            {"value": 1, "label": "Sporadic"}, {"value": 1, "label": "Sporadic"}])

    def test_sporadic_morn_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Quite a bit,Sporadic,"")'}, {'row': '(2020-08-31,A little bit,Morning,"")'}, 
            {'row': '(2020-08-31,Very much,Daytime,"")'}, {'row': '(2020-08-31,Somewhat,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Sporadic"}, 
            {"value": 3, "label": "Sporadic"}, {"value": 3, "label": "Sporadic"}, {"value": 1, "label": "Morning"}, 
            {"value": 4, "label": "Daytime"}, {"value": 2, "label": "Night-time"}])

    def test_sporadic_morn_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Quite a bit,Sporadic,"")'}, {'row': '(2020-08-31,Not at all,Morning,"")'},
            {'row': '(2020-08-31,Quite a bit,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Sporadic"}, 
            {"value": 3, "label": "Sporadic"}, {"value": 3, "label": "Sporadic"}, {"value": 0, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, None])

    def test_sporadic_morn_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Quite a bit,Sporadic,"")'}, {'row': '(2020-08-31,Not at all,Morning,"")'},
            {'row': '(2020-08-31,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Sporadic"}, 
            {"value": 3, "label": "Sporadic"}, {"value": 3, "label": "Sporadic"}, {"value": 0, "label": "Morning"},
            None, {"value": 3, "label": "Night-time"}])

    def test_sporadic_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Quite a bit,Sporadic,"")'}, {'row': '(2020-08-31,Not at all,Daytime,"")'}, 
        {'row': '(2020-08-31,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Sporadic"}, {"value": 3, "label": "Sporadic"}, 
            {"value": 3, "label": "Sporadic"}, None, {"value": 0, "label": "Daytime"},
            {"value": 3, "label": "Night-time"}])

    def test_sporadic_morn(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Quite a bit,Sporadic,"")'}, {'row': '(2020-08-31,Not at all,Morning,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Sporadic"}, {"value": 3, "label": "Sporadic"}, 
            {"value": 3, "label": "Sporadic"}, {"value": 0, "label": "Morning"}, None, None])

    def test_sporadic_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Quite a bit,Sporadic,"")'}, {'row': '(2020-08-31,Not at all,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Sporadic"}, {"value": 3, "label": "Sporadic"}, 
            {"value": 3, "label": "Sporadic"}, None, {"value": 0, "label": "Daytime"}, None])

    def test_sporadic_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Quite a bit,Sporadic,"")'}, {'row': '(2020-08-31,Not at all,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Sporadic"}, {"value": 3, "label": "Sporadic"}, 
            {"value": 3, "label": "Sporadic"}, None, None, {"value": 0, "label": "Night-time"}])
    
    def test_morn_day_night_all_the_time(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Daytime,"")'}, 
        {'row': '(2020-08-30,Not at all,Night-time,"")'}, {'row': '(2020-08-31,A little bit,All the time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, {"value": 2, "label": "Daytime"}, 
            {"value": 0, "label": "Night-time"}, {"value": 1, "label": "Morning"}, {"value": 1, "label": "Daytime"}, 
            {"value": 1, "label": "Night-time"}])

    def test_morn_day_night_sporadic(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Daytime,"")'}, 
        {'row': '(2020-08-30,Not at all,Night-time,"")'}, {'row': '(2020-08-31,A little bit,Sporadic,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, {"value": 2, "label": "Daytime"}, 
            {"value": 0, "label": "Night-time"}, {"value": 1, "label": "Sporadic"}, {"value": 1, "label": "Sporadic"}, 
            {"value": 1, "label": "Sporadic"}])

    def test_morn_day_night_morn_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Daytime,"")'}, 
        {'row': '(2020-08-30,Not at all,Night-time,"")'}, {'row': '(2020-08-31,A little bit,Morning,"")'}, 
            {'row': '(2020-08-31,Very much,Daytime,"")'}, {'row': '(2020-08-31,Somewhat,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, {"value": 2, "label": "Daytime"}, 
            {"value": 0, "label": "Night-time"}, {"value": 1, "label": "Morning"}, 
            {"value": 4, "label": "Daytime"}, {"value": 2, "label": "Night-time"}])

    def test_morn_day_night_morn_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Daytime,"")'}, 
        {'row': '(2020-08-30,Not at all,Night-time,"")'}, {'row': '(2020-08-31,Not at all,Morning,"")'},
            {'row': '(2020-08-31,Quite a bit,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, {"value": 2, "label": "Daytime"}, 
            {"value": 0, "label": "Night-time"}, {"value": 0, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, None])

    def test_morn_day_night_morn_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Daytime,"")'}, 
        {'row': '(2020-08-30,Not at all,Night-time,"")'}, {'row': '(2020-08-31,Not at all,Morning,"")'},
            {'row': '(2020-08-31,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, {"value": 2, "label": "Daytime"}, 
            {"value": 0, "label": "Night-time"}, {"value": 0, "label": "Morning"},
            None, {"value": 3, "label": "Night-time"}])

    def test_morn_day_night_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Daytime,"")'}, 
        {'row': '(2020-08-30,Not at all,Night-time,"")'}, {'row': '(2020-08-31,Not at all,Daytime,"")'}, 
        {'row': '(2020-08-31,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, {"value": 2, "label": "Daytime"}, 
            {"value": 0, "label": "Night-time"}, None, {"value": 0, "label": "Daytime"},
            {"value": 3, "label": "Night-time"}])

    def test_morn_day_night_morn(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Daytime,"")'}, 
        {'row': '(2020-08-30,Not at all,Night-time,"")'}, {'row': '(2020-08-31,Not at all,Morning,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, {"value": 2, "label": "Daytime"}, 
            {"value": 0, "label": "Night-time"}, {"value": 0, "label": "Morning"}, None, None])

    def test_morn_day_night_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Daytime,"")'}, 
        {'row': '(2020-08-30,Not at all,Night-time,"")'}, {'row': '(2020-08-31,Not at all,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, {"value": 2, "label": "Daytime"}, 
            {"value": 0, "label": "Night-time"}, None, {"value": 0, "label": "Daytime"}, None])

    def test_morn_day_night_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Daytime,"")'}, 
        {'row': '(2020-08-30,Not at all,Night-time,"")'}, {'row': '(2020-08-31,Not at all,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, {"value": 2, "label": "Daytime"}, 
            {"value": 0, "label": "Night-time"}, None, None, {"value": 0, "label": "Night-time"}])

    def test_morn_day_all_the_time(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Daytime,"")'}, 
        {'row': '(2020-08-31,A little bit,All the time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, {"value": 2, "label": "Daytime"}, None,
            {"value": 1, "label": "Morning"}, {"value": 1, "label": "Daytime"}, 
            {"value": 1, "label": "Night-time"}])

    def test_morn_day_sporadic(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Daytime,"")'}, 
            {'row': '(2020-08-31,A little bit,Sporadic,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, {"value": 2, "label": "Daytime"}, None,
            {"value": 1, "label": "Sporadic"}, {"value": 1, "label": "Sporadic"}, 
            {"value": 1, "label": "Sporadic"}])

    def test_morn_day_morn_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Daytime,"")'},
            {'row': '(2020-08-31,A little bit,Morning,"")'}, 
            {'row': '(2020-08-31,Very much,Daytime,"")'}, {'row': '(2020-08-31,Somewhat,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, {"value": 2, "label": "Daytime"}, None, 
            {"value": 1, "label": "Morning"}, 
            {"value": 4, "label": "Daytime"}, {"value": 2, "label": "Night-time"}])

    def test_morn_day_morn_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Daytime,"")'}, 
        {'row': '(2020-08-31,Not at all,Morning,"")'},
            {'row': '(2020-08-31,Quite a bit,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, {"value": 2, "label": "Daytime"}, None, 
            {"value": 0, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, None])

    def test_morn_day_morn_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Daytime,"")'}, 
            {'row': '(2020-08-31,Not at all,Morning,"")'},
            {'row': '(2020-08-31,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, {"value": 2, "label": "Daytime"}, None, 
            {"value": 0, "label": "Morning"},
            None, {"value": 3, "label": "Night-time"}])

    def test_morn_day_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Daytime,"")'}, 
        {'row': '(2020-08-31,Not at all,Daytime,"")'}, 
        {'row': '(2020-08-31,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, {"value": 2, "label": "Daytime"}, None, 
            None, {"value": 0, "label": "Daytime"},
            {"value": 3, "label": "Night-time"}])

    def test_morn_day_morn(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Daytime,"")'}, 
        {'row': '(2020-08-31,Not at all,Morning,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, {"value": 2, "label": "Daytime"}, None, 
            {"value": 0, "label": "Morning"}, None, None])

    def test_morn_day_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Daytime,"")'},
            {'row': '(2020-08-31,Not at all,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, {"value": 2, "label": "Daytime"}, None, 
            None, {"value": 0, "label": "Daytime"}, None])

    def test_morn_day_night_2(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Daytime,"")'},
            {'row': '(2020-08-31,Not at all,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, {"value": 2, "label": "Daytime"}, None, 
            None, None, {"value": 0, "label": "Night-time"}])

    def test_morn_night_all_the_time(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'}, 
        {'row': '(2020-08-31,A little bit,All the time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, {"value": 2, "label": "Night-time"},
            {"value": 1, "label": "Morning"}, {"value": 1, "label": "Daytime"}, 
            {"value": 1, "label": "Night-time"}])

    def test_morn_night_sporadic(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'}, 
            {'row': '(2020-08-31,A little bit,Sporadic,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, {"value": 2, "label": "Night-time"},
            {"value": 1, "label": "Sporadic"}, {"value": 1, "label": "Sporadic"}, 
            {"value": 1, "label": "Sporadic"}])

    def test_morn_night_morn_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'},
            {'row': '(2020-08-31,A little bit,Morning,"")'}, 
            {'row': '(2020-08-31,Very much,Daytime,"")'}, {'row': '(2020-08-31,Somewhat,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, {"value": 2, "label": "Night-time"}, 
            {"value": 1, "label": "Morning"}, 
            {"value": 4, "label": "Daytime"}, {"value": 2, "label": "Night-time"}])

    def test_morn_night_morn_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'}, 
        {'row': '(2020-08-31,Not at all,Morning,"")'},
            {'row': '(2020-08-31,Quite a bit,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, {"value": 2, "label": "Night-time"}, 
            {"value": 0, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, None])

    def test_morn_night_morn_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'}, 
            {'row': '(2020-08-31,Not at all,Morning,"")'},
            {'row': '(2020-08-31,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, {"value": 2, "label": "Night-time"}, 
            {"value": 0, "label": "Morning"},
            None, {"value": 3, "label": "Night-time"}])

    def test_morn_night_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'}, 
        {'row': '(2020-08-31,Not at all,Daytime,"")'}, 
        {'row': '(2020-08-31,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, {"value": 2, "label": "Night-time"}, 
            None, {"value": 0, "label": "Daytime"},
            {"value": 3, "label": "Night-time"}])

    def test_morn_night_morn(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'}, 
        {'row': '(2020-08-31,Not at all,Morning,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, {"value": 2, "label": "Night-time"}, 
            {"value": 0, "label": "Morning"}, None, None])

    def test_morn_night_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'},
            {'row': '(2020-08-31,Not at all,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, {"value": 2, "label": "Night-time"}, 
            None, {"value": 0, "label": "Daytime"}, None])

    def test_morn_night_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'},
            {'row': '(2020-08-31,Not at all,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, {"value": 2, "label": "Night-time"}, 
            None, None, {"value": 0, "label": "Night-time"}])

    def test_day_night_all_the_time(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Daytime,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'}, 
        {'row': '(2020-08-31,A little bit,All the time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, {"value": 4, "label": "Daytime"}, {"value": 2, "label": "Night-time"},
            {"value": 1, "label": "Morning"}, {"value": 1, "label": "Daytime"}, 
            {"value": 1, "label": "Night-time"}])

    def test_day_night_sporadic(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Daytime,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'}, 
            {'row': '(2020-08-31,A little bit,Sporadic,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, {"value": 4, "label": "Daytime"}, {"value": 2, "label": "Night-time"},
            {"value": 1, "label": "Sporadic"}, {"value": 1, "label": "Sporadic"}, 
            {"value": 1, "label": "Sporadic"}])

    def test_day_night_morn_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Daytime,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'},
            {'row': '(2020-08-31,A little bit,Morning,"")'}, 
            {'row': '(2020-08-31,Very much,Daytime,"")'}, {'row': '(2020-08-31,Somewhat,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, {"value": 4, "label": "Daytime"}, {"value": 2, "label": "Night-time"}, 
            {"value": 1, "label": "Morning"}, 
            {"value": 4, "label": "Daytime"}, {"value": 2, "label": "Night-time"}])

    def test_day_night_morn_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Daytime,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'}, 
        {'row': '(2020-08-31,Not at all,Morning,"")'},
            {'row': '(2020-08-31,Quite a bit,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, {"value": 4, "label": "Daytime"}, {"value": 2, "label": "Night-time"}, 
            {"value": 0, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, None])

    def test_day_night_morn_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Daytime,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'}, 
            {'row': '(2020-08-31,Not at all,Morning,"")'},
            {'row': '(2020-08-31,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, {"value": 4, "label": "Daytime"}, {"value": 2, "label": "Night-time"}, 
            {"value": 0, "label": "Morning"},
            None, {"value": 3, "label": "Night-time"}])

    def test_day_night_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Daytime,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'}, 
        {'row': '(2020-08-31,Not at all,Daytime,"")'}, 
        {'row': '(2020-08-31,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, {"value": 4, "label": "Daytime"}, {"value": 2, "label": "Night-time"}, 
            None, {"value": 0, "label": "Daytime"},
            {"value": 3, "label": "Night-time"}])

    def test_day_night_morn(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Daytime,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'}, 
        {'row': '(2020-08-31,Not at all,Morning,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, {"value": 4, "label": "Daytime"}, {"value": 2, "label": "Night-time"}, 
            {"value": 0, "label": "Morning"}, None, None])

    def test_day_night_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Daytime,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'},
            {'row': '(2020-08-31,Not at all,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, {"value": 4, "label": "Daytime"}, {"value": 2, "label": "Night-time"}, 
            None, {"value": 0, "label": "Daytime"}, None])

    def test_day_night_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Daytime,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'},
            {'row': '(2020-08-31,Not at all,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, {"value": 4, "label": "Daytime"}, {"value": 2, "label": "Night-time"}, 
            None, None, {"value": 0, "label": "Night-time"}])

    def test_morn_all_the_time(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, 
        {'row': '(2020-08-31,A little bit,All the time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, None,
            {"value": 1, "label": "Morning"}, {"value": 1, "label": "Daytime"}, 
            {"value": 1, "label": "Night-time"}])

    def test_morn_sporadic(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, 
            {'row': '(2020-08-31,A little bit,Sporadic,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, None,
            {"value": 1, "label": "Sporadic"}, {"value": 1, "label": "Sporadic"}, 
            {"value": 1, "label": "Sporadic"}])

    def test_morn_morn_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'},
            {'row': '(2020-08-31,A little bit,Morning,"")'}, 
            {'row': '(2020-08-31,Very much,Daytime,"")'}, {'row': '(2020-08-31,Somewhat,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, None, 
            {"value": 1, "label": "Morning"}, 
            {"value": 4, "label": "Daytime"}, {"value": 2, "label": "Night-time"}])

    def test_morn_morn_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, 
        {'row': '(2020-08-31,Not at all,Morning,"")'},
            {'row': '(2020-08-31,Quite a bit,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, None, 
            {"value": 0, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, None])

    def test_morn_morn_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, 
            {'row': '(2020-08-31,Not at all,Morning,"")'},
            {'row': '(2020-08-31,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, None, 
            {"value": 0, "label": "Morning"},
            None, {"value": 3, "label": "Night-time"}])

    def test_morn_day_night_3(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, 
        {'row': '(2020-08-31,Not at all,Daytime,"")'}, 
        {'row': '(2020-08-31,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, None, 
            None, {"value": 0, "label": "Daytime"},
            {"value": 3, "label": "Night-time"}])

    def test_morn_morn(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, 
        {'row': '(2020-08-31,Not at all,Morning,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, None, 
            {"value": 0, "label": "Morning"}, None, None])

    def test_morn_day_2(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'},
            {'row': '(2020-08-31,Not at all,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, None, 
            None, {"value": 0, "label": "Daytime"}, None])

    def test_morn_night_2(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'},
            {'row': '(2020-08-31,Not at all,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, None, 
            None, None, {"value": 0, "label": "Night-time"}])

    def test_day_all_the_time(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Daytime,"")'}, 
        {'row': '(2020-08-31,A little bit,All the time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, {"value": 4, "label": "Daytime"}, None,
            {"value": 1, "label": "Morning"}, {"value": 1, "label": "Daytime"}, 
            {"value": 1, "label": "Night-time"}])

    def test_day_sporadic(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Daytime,"")'}, 
            {'row': '(2020-08-31,A little bit,Sporadic,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, {"value": 4, "label": "Daytime"}, None,
            {"value": 1, "label": "Sporadic"}, {"value": 1, "label": "Sporadic"}, 
            {"value": 1, "label": "Sporadic"}])

    def test_day_morn_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Daytime,"")'},
            {'row': '(2020-08-31,A little bit,Morning,"")'}, 
            {'row': '(2020-08-31,Very much,Daytime,"")'}, {'row': '(2020-08-31,Somewhat,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, {"value": 4, "label": "Daytime"}, None, 
            {"value": 1, "label": "Morning"}, 
            {"value": 4, "label": "Daytime"}, {"value": 2, "label": "Night-time"}])

    def test_day_morn_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Daytime,"")'}, 
        {'row': '(2020-08-31,Not at all,Morning,"")'},
            {'row': '(2020-08-31,Quite a bit,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, {"value": 4, "label": "Daytime"}, None, 
            {"value": 0, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, None])

    def test_day_morn_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Daytime,"")'}, 
            {'row': '(2020-08-31,Not at all,Morning,"")'},
            {'row': '(2020-08-31,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, {"value": 4, "label": "Daytime"}, None, 
            {"value": 0, "label": "Morning"},
            None, {"value": 3, "label": "Night-time"}])

    def test_day_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Daytime,"")'}, 
        {'row': '(2020-08-31,Not at all,Daytime,"")'}, 
        {'row': '(2020-08-31,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, {"value": 4, "label": "Daytime"}, None, 
            None, {"value": 0, "label": "Daytime"},
            {"value": 3, "label": "Night-time"}])

    def test_day_morn(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Daytime,"")'}, 
        {'row': '(2020-08-31,Not at all,Morning,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, {"value": 4, "label": "Daytime"}, None,  
            {"value": 0, "label": "Morning"}, None, None])

    def test_day_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Daytime,"")'},
            {'row': '(2020-08-31,Not at all,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, {"value": 4, "label": "Daytime"}, None, 
            None, {"value": 0, "label": "Daytime"}, None])

    def test_day_night_2(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Daytime,"")'},
            {'row': '(2020-08-31,Not at all,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, {"value": 4, "label": "Daytime"}, None,  
            None, None, {"value": 0, "label": "Night-time"}])

    def test_night_all_the_time(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Night-time,"")'}, 
        {'row': '(2020-08-31,A little bit,All the time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, None, {"value": 4, "label": "Night-time"},
            {"value": 1, "label": "Morning"}, {"value": 1, "label": "Daytime"}, 
            {"value": 1, "label": "Night-time"}])

    def test_night_sporadic(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Night-time,"")'}, 
            {'row': '(2020-08-31,A little bit,Sporadic,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, None, {"value": 4, "label": "Night-time"},
            {"value": 1, "label": "Sporadic"}, {"value": 1, "label": "Sporadic"}, 
            {"value": 1, "label": "Sporadic"}])

    def test_night_morn_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Night-time,"")'},
            {'row': '(2020-08-31,A little bit,Morning,"")'}, 
            {'row': '(2020-08-31,Very much,Daytime,"")'}, {'row': '(2020-08-31,Somewhat,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, None, {"value": 4, "label": "Night-time"},
            {"value": 1, "label": "Morning"}, 
            {"value": 4, "label": "Daytime"}, {"value": 2, "label": "Night-time"}])

    def test_night_morn_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Night-time,"")'}, 
        {'row': '(2020-08-31,Not at all,Morning,"")'},
            {'row': '(2020-08-31,Quite a bit,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, None, {"value": 4, "label": "Night-time"},
            {"value": 0, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, None])

    def test_night_morn_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Night-time,"")'}, 
            {'row': '(2020-08-31,Not at all,Morning,"")'},
            {'row': '(2020-08-31,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, None, {"value": 4, "label": "Night-time"}, 
            {"value": 0, "label": "Morning"},
            None, {"value": 3, "label": "Night-time"}])

    def test_night_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Night-time,"")'}, 
        {'row': '(2020-08-31,Not at all,Daytime,"")'}, 
        {'row': '(2020-08-31,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, None, {"value": 4, "label": "Night-time"}, 
            None, {"value": 0, "label": "Daytime"},
            {"value": 3, "label": "Night-time"}])

    def test_night_morn(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Night-time,"")'}, 
        {'row': '(2020-08-31,Not at all,Morning,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, None, {"value": 4, "label": "Night-time"},  
            {"value": 0, "label": "Morning"}, None, None])

    def test_night_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Night-time,"")'},
            {'row': '(2020-08-31,Not at all,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, None, {"value": 4, "label": "Night-time"}, 
            None, {"value": 0, "label": "Daytime"}, None])

    def test_night_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 8, 31)
        data = [{'row': '(2020-08-30,Very much,Night-time,"")'},
            {'row': '(2020-08-31,Not at all,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31", "2020-08-31\n"])
        self.assertEqual(severity, [None, None, {"value": 4, "label": "Night-time"},
            None, None, {"value": 0, "label": "Night-time"}])

    def test_all_the_time_break_sporadic(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 9, 1)
        data = [{'row': '(2020-08-30,Quite a bit,All the time,"")'}, {'row': '(2020-09-01,A little bit,Sporadic,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31",
         "2020-08-31\n", "2020-09-01 ", "2020-09-01", "2020-09-01\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, {"value": 3, "label": "Night-time"}, None, None, None, {"value": 1, "label": "Sporadic"}, 
            {"value": 1, "label": "Sporadic"}, {"value": 1, "label": "Sporadic"}])

    def test_morn_day_night_break_morn_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 9, 1)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Daytime,"")'}, 
        {'row': '(2020-08-30,Not at all,Night-time,"")'}, {'row': '(2020-09-01,Not at all,Morning,"")'},
            {'row': '(2020-09-01,Quite a bit,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31",
         "2020-08-31\n", "2020-09-01 ", "2020-09-01", "2020-09-01\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, {"value": 2, "label": "Daytime"}, 
            {"value": 0, "label": "Night-time"}, None, None, None, {"value": 0, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, None])

    def test_morn_night_break_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 9, 1)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'}, 
        {'row': '(2020-09-01,Not at all,Daytime,"")'}, 
        {'row': '(2020-09-01,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31",
            "2020-08-31\n", "2020-09-01 ", "2020-09-01", "2020-09-01\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, {"value": 2, "label": "Night-time"}, None, 
            None, None, None, {"value": 0, "label": "Daytime"}, {"value": 3, "label": "Night-time"}])

    def test_all_the_time_break_break_morn_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 9, 2)
        data = [{'row': '(2020-08-30,Quite a bit,All the time,"")'}, {'row': '(2020-09-01,A little bit,Morning,"")'}, 
            {'row': '(2020-09-02,Very much,Daytime,"")'}, {'row': '(2020-09-02,Somewhat,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31",
            "2020-08-31\n", "2020-09-01 ", "2020-09-01", "2020-09-01\n", "2020-09-02 ", "2020-09-02", "2020-09-02\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, {"value": 3, "label": "Night-time"}, None, None, None, None, None, None,
            {"value": 1, "label": "Morning"}, {"value": 4, "label": "Daytime"}, {"value": 2, "label": "Night-time"}])

    def test_all_the_time_break_break_morn_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 9, 2)
        data = [{'row': '(2020-08-30,Quite a bit,All the time,"")'}, {'row': '(2020-09-02,A little bit,Morning,"")'}, 
            {'row': '(2020-09-02,Very much,Daytime,"")'}, {'row': '(2020-09-02,Somewhat,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31",
            "2020-08-31\n", "2020-09-01 ", "2020-09-01", "2020-09-01\n", "2020-09-02 ", "2020-09-02", "2020-09-02\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, {"value": 3, "label": "Night-time"}, None, None, None, None, None, None,
            {"value": 1, "label": "Morning"}, {"value": 4, "label": "Daytime"}, {"value": 2, "label": "Night-time"}])

    def test_morn_day_break_break_day_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 9, 2)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Daytime,"")'}, 
        {'row': '(2020-09-02,Not at all,Daytime,"")'}, 
        {'row': '(2020-09-02,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31",
            "2020-08-31\n", "2020-09-01 ", "2020-09-01", "2020-09-01\n", "2020-09-02 ", "2020-09-02", "2020-09-02\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, {"value": 2, "label": "Daytime"}, None, 
            None, None, None, None, None, None, None, {"value": 0, "label": "Daytime"},
            {"value": 3, "label": "Night-time"}])

    def test_morn_break_break_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 9, 2)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'},
            {'row': '(2020-09-02,Not at all,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31",
            "2020-08-31\n", "2020-09-01 ", "2020-09-01", "2020-09-01\n", "2020-09-02 ", "2020-09-02", "2020-09-02\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, None, None, None, None, None, None, None,
            None, None, {"value": 0, "label": "Night-time"}])

    def test_sporadic_break_break_break_morn_day(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 9, 3)
        data = [{'row': '(2020-08-30,Quite a bit,Sporadic,"")'}, {'row': '(2020-09-03,Not at all,Morning,"")'},
            {'row': '(2020-09-03,Quite a bit,Daytime,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31",
            "2020-08-31\n", "2020-09-01 ", "2020-09-01", "2020-09-01\n", "2020-09-02 ", "2020-09-02", "2020-09-02\n",
            "2020-09-03 ", "2020-09-03", "2020-09-03\n"])
        self.assertEqual(severity, [{"value": 3, "label": "Sporadic"}, 
            {"value": 3, "label": "Sporadic"}, {"value": 3, "label": "Sporadic"}, None, None, None, None, None, None, 
            None, None, None, {"value": 0, "label": "Morning"}, 
            {"value": 3, "label": "Daytime"}, None])

    def test_morn_night_break_break_break_morn(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 9, 3)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'}, 
        {'row': '(2020-09-03,Not at all,Morning,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31",
            "2020-08-31\n", "2020-09-01 ", "2020-09-01", "2020-09-01\n", "2020-09-02 ", "2020-09-02", "2020-09-02\n",
            "2020-09-03 ", "2020-09-03", "2020-09-03\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, {"value": 2, "label": "Night-time"}, None, 
            None, None, None, None, None, None, None, None, {"value": 0, "label": "Morning"}, None, None])

    def test_morn_night_break_morn_break_night(self):
        start_date = datetime(2020, 8, 30)
        end_date = datetime(2020, 9, 3)
        data = [{'row': '(2020-08-30,Very much,Morning,"")'}, {'row': '(2020-08-30,Somewhat,Night-time,"")'}, 
            {'row': '(2020-09-01,Not at all,Morning,"")'},
            {'row': '(2020-09-03,Quite a bit,Night-time,"")'}]
        date, severity = clean_data(start_date, end_date, data)
        self.assertEqual(date, ["2020-08-30 ", "2020-08-30", "2020-08-30\n", "2020-08-31 ", "2020-08-31",
            "2020-08-31\n", "2020-09-01 ", "2020-09-01", "2020-09-01\n", "2020-09-02 ", "2020-09-02", "2020-09-02\n",
            "2020-09-03 ", "2020-09-03", "2020-09-03\n"])
        self.assertEqual(severity, [{"value": 4, "label": "Morning"}, None, {"value": 2, "label": "Night-time"}, None, 
            None, None, {"value": 0, "label": "Morning"}, None, None, None, None, None, None, None, {"value": 3, "label": "Night-time"}])


if __name__ == '__main__':
    unittest.main()