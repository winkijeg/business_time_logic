import pandas as pd

import datetime
import pytz
import businesstimedelta

# iso code for Germany DE, province Berlin BE
import holidays as pyholidays

tz_berlin = pytz.timezone('Europe/Berlin')


def b_difference(t1, t2):
    return businesshrs.difference(t1, t2)


def b_difference_minutes(t1, t2):
    b_diff = businesshrs.difference(t1, t2)
    return (b_diff.hours * 60) + (b_diff.seconds / 60)


def b_difference_tps(t1, t2):
    b_diff = businesshrs.difference(t1, t2)
    return round(((b_diff.hours * 60) + (b_diff.seconds / 60)) / 15)


# Define local holidays
ber_holidays = pyholidays.DE(prov='BE')
holidays = businesstimedelta.HolidayRule(
    ber_holidays,
    tz=tz_berlin
)

# Define a working day
workday = businesstimedelta.WorkDayRule(
    start_time=datetime.time(9),
    end_time=datetime.time(17, 30),
    working_days=[0, 1, 2, 3, 4],
    tz=tz_berlin
)

 # Take out the lunch break
lunchbreak = businesstimedelta.LunchTimeRule(
    start_time=datetime.time(13),
    end_time=datetime.time(13, 30),
    working_days=[0, 1, 2, 3, 4],
    tz=tz_berlin
)

# Combine the two
businesshrs = businesstimedelta.Rules([workday, lunchbreak, holidays])


# -----------------------

data = {'start_date': ['03-07-2022', '03-08-2022', '03-09-2022', '03-10-2022', '03-11-2022', '03-11-2022'],
        'start_time': ['15:00:00', '15:00:00', '15:00:00', '15:00:00', '16:01:00', '08:00:00'],
        'end_date': ['03-08-2022', '03-09-2022', '03-10-2022', '03-11-2022', '03-14-2022', '03-11-2022'],
        'end_time': ['09:00:00', '09:00:00', '09:00:00', '09:00:00', '09:00:00', '16:00:00']
        }

df = pd.DataFrame(data)

df["start_dt_1"] = pd.to_datetime(df['start_date'] + ' ' + df['start_time'], utc=True).dt.tz_convert('Europe/Berlin')
df["end_dt_1"] = pd.to_datetime(df['end_date'] + ' ' + df['end_time'], utc=True).dt.tz_convert('Europe/Berlin')

df['b_diff'] = df.apply (lambda row: b_difference(row["start_dt_1"], row["end_dt_1"]), axis=1)
df['b_diff_min'] = df.apply (lambda row: b_difference_minutes(row["start_dt_1"], row["end_dt_1"]), axis=1)
df['b_diff_tp'] = df.apply (lambda row: b_difference_tps(row["start_dt_1"], row["end_dt_1"]), axis=1)

print(df)

