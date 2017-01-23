#!/usr/bin/env python

# Script to import some test data into the db. Usually we should get a warning
# due to the bad formatting of the date, which is missing the time zone flag.

# Execute this directly into the django shell.

from weather_station_app.models import Record, Channel, User
from datetime import datetime

u = User("test", "test@example.com", datetime.now())

c = Channel("test", u, 12345678, datetime.now())

with open("sample_thingspeak_no_header.csv") as fo:
  for line in fo:
    line = line.strip().split(',')
    dt, id, t, h = line
    dt, t, h = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S UTC'), float(t), float(h)
    r = Record(channel=c, insertion_time=dt, id=id, field1=t, field2=h)
    r.save()
