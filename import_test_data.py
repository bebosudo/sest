#!/usr/bin/env python

# Script to import some test data into the db. Usually we should get a warning
# due to the bad formatting of the date, which is missing the time zone flag.

# Copy and execute this directly into the django shell.

from weather_station_app.models import *
from django.utils import timezone
from datetime import datetime

u = User.objects.create(nick="test", email="test@example.com",
                        registration_time=timezone.now())

# c = Channel(title="test", user=u, 12345678, datetime.now())
c = Channel.objects.create(user=u, last_update=timezone.now(), number_fields=2)
c.fieldencoding_set.create(field_no=1, encoding='float')
c.fieldencoding_set.create(field_no=2, encoding='float')

with open("sample_thingspeak_no_header.csv") as fo:
    for line in fo:
        line = line.strip().split(',')
        dt, _id, t, h = line
        dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S UTC')
        t, h = float(t), float(h)
        r = Record.objects.create(channel=c, insertion_time=dt, id=_id)
        r.field_set.create(field_no=1, value=t)
        r.field_set.create(field_no=2, value=h)
