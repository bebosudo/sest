#!/usr/bin/env python

# Script to import some test data into the db. Usually we should get a warning
# due to the bad formatting of the date, which is missing the time zone flag.

# Copy and execute this directly into the django shell.

from sest.models import *
from datetime import datetime

u = User.objects.create(username="test", email="test@example.com")

# c = Channel(title="test", user=u, 12345678, datetime.now())
c = Channel.objects.create(user=u, number_fields=2)
c.fieldencoding_set.create(field_no=1, encoding='float')
c.fieldencoding_set.create(field_no=2, encoding='float')

with open("sample_without_header.csv") as fo:
    for line in fo:
        line = line.strip().split(',')
        dt, _id, t, h = line
        dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S UTC')
        t, h = float(t), float(h)
        r = Record.objects.create(channel=c, insertion_time=dt, id=_id)
        r.field_set.create(field_no=1, val=t)
        r.field_set.create(field_no=2, val=h)
