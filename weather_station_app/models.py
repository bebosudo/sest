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
    MAX_NUMBER_FIELDS = 3

    # An autoincrement field called `id' is automatically provided by django.
    title = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    last_update = models.DateTimeField(blank=True)
    description = models.TextField(max_length=500, blank=True)
    # TODO: create a method that allows the user to regenerate another uuid.
    write_key = models.UUIDField(default=uuid.uuid4, editable=False)
    number_fields = models.PositiveSmallIntegerField()

    def __str__(self):
        return "{} (created by user: '{}')".format(str(self.id),
                                                   repr(self.user))

    def get_type(self, field_no):
        return self.fieldencoding_set.get(field_no=field_no).encoding


class FieldEncoding(models.Model):
    """Store the encoding used for each field the user registers, in order to
    recreate the original value.
    """
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    field_no = models.PositiveSmallIntegerField()
    encoding = models.CharField(max_length=50)


class Record(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    insertion_time = models.DateTimeField('registration date and time')

    def __str__(self):
        return self.insertion_time.strftime('%Y-%m-%d %H:%M:%S %Z')


class Field(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    field_no = models.PositiveSmallIntegerField()
    # We save every field value as a string, and then we use a function defined
    # by the user inside each channel to restore the original meaning of the
    # value.
    value = models.CharField(max_length=100)

    def __str__(self):
        return "{} - {}".format(self.record, self.value)

    def get_real_value(self):
        encoding = self.record.channel.get_type(field_no=self.field_no)

        # This changes the default exception error to something more
        # verbose.

        # TODO: provide a safe way to save the encoding at the Channel level,
        # and make sure that the values are checked also at the saving.
        try:
            if encoding == "float":
                return float(self.value)
            elif encoding == "int":
                return int(self.value)
        except ValueError:
            # If an incorrect value has been saved as a string into the DB:
            raise ValueError("Wrong encoding for the field no. {}, which is "
                             "part of the channel {}. Encoding proposed: '{}';"
                             " example of a value saved: '{}'.".format(
                                 self.field_no,
                                 self.record.channel,
                                 encoding,
                                 self.value,
                             )
                             )
        else:
            # If no decoding operations are defined to restore the value:
            raise ValueError("No decoding operation defined in order to "
                             "restore values at position no. {} of the channel"
                             " {}. Encoding proposed: '{}'; example of a value"
                             " saved: '{}'.".format(
                                 self.field_no,
                                 self.record.channel,
                                 encoding,
                                 self.value,
                             )
                             )
