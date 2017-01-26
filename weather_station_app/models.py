from django.db import models

# from datetime import datetime
import uuid


class User(models.Model):
    nick = models.CharField(max_length=50, primary_key=True)
    email = models.EmailField()
    registration_time = models.DateField()

    def __str__(self):
        return self.nick


class Channel(models.Model):
    # `id' field is automatically provided by django, but I prefer to state it.
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update = models.DateTimeField(blank=True)
    description = models.TextField(max_length=500, blank=True)
    # TODO: create a method that allows the user to regenerate another uuid.
    write_key = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return "{} (created by user: '{}')".format(str(self.id), repr(self.user))


class Record(models.Model):
    # autoincrement field is automatically provided by django.
    # id = models.AutoField(primary_key=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    insertion_time = models.DateTimeField('registration date and time')
    # field1 = models.FloatField('temperature')
    # field2 = models.FloatField('humidity')
    MAX_NUMBER_FIELDS = 3


    def __str__(self):
        return self.insertion_time.strftime('%Y-%m-%d %H:%M:%S %Z')


class Field(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    field_no = models.IntegerField()
    value = models.FloatField()

    def __str__(self):
        return "{} - {}".format(self.record, self.value)
