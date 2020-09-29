import datetime

from pytz import timezone


# Time format to make test on windows.
tz = timezone("Europe/Rome")
test_time = tz.localize(datetime.datetime(year=2020,
                                          month=9,
                                          day=28,
                                          hour=15,
                                          minute=31,
                                          second=55
                                          )).timetz()


# Time for automatic functions
every_day = datetime.time(hour=0, minute=0, second=1)

