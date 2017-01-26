#!/usr/bin/env python

# Script to import some test data into the db. Usually we should get a warning
# due to the bad formatting of the date, which is missing the time zone flag.

# Copy and execute this directly into the django shell.

from weather_station_app.models import Record, Channel, User, Field
from django.utils import timezone
from datetime import datetime

u = User.objects.create(nick="test", email="test@example.com",
                        registration_time=timezone.now())

# c = Channel(title="test", user=u, 12345678, datetime.now())
c = Channel.objects.create(user=u, last_update=timezone.now())

with open("sample_thingspeak_no_header.csv") as fo:
    for line in fo:
        line = line.strip().split(',')
        dt, _id, t, h = line
        dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S UTC')
        t, h = float(t), float(h)
        r = Record.objects.create(channel=c, insertion_time=dt, id=_id)
        f1 = Field.objects.create(record=r, field_no=1, value=t)
        f2 = Field.objects.create(record=r, field_no=2, value=h)

