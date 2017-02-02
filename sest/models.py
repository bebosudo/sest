from django.db import models

from email import send_email_wrapper

# from datetime import datetime
import uuid
import operator as op
from itertools import product


class User(models.Model):
    nick = models.CharField(max_length=50, primary_key=True)
    email = models.EmailField()
    registration_time = models.DateField()

    def __str__(self):
        return self.nick


class NotificationEmail(models.Model):
    """Stores user's emails to which send channel activities.

    These objects are different from the email field of the user, because
    a user could choose to send notifications/alerts to different emails (and
    for example not to the one used to register to the service) for each
    channel he creates.
    By design, only a single email can be used to communicate with
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # This address should be validated, to make sure that the user really owns
    # the email address he declares.
    address = models.EmailField(primary_key=True)


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

    notification_email = models.ForeignKey(NotificationEmail,
                                           blank=True, null=True,
                                           on_delete=models.CASCADE)

    def __str__(self):
        return "{} (created by user: '{}')".format(str(self.id),
                                                   repr(self.user))

    @property
    def get_encoding(self, field_no):
        return self.fieldencoding_set.get(field_no=field_no).encoding

    def send_email(self, message):
        if not self.notification_email:
            raise ValueError("No email connected to the "
                             "channel {}.".format(self))

        send_email_wrapper(to_list=[self.notification_email],
                           subject="Alert. Condition validated on channel "
                           "{}".format(self),
                           text_body=message)

    def check_and_react(self, record_to_check):
        for cond, f in product(self.conditionandreaction_set.all(),
                               record_to_check.field_set.all()):
            reaction = cond.check_condition(f)
            if reaction:
                # If a condition is validated, trigger the relative action and
                # then quit the execution.
                cond.react(record_to_check)
                return True

        return False


class FieldEncoding(models.Model):
    """Store the encoding used for each field the user registers, in order to
    recreate the original value.
    """

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    field_no = models.PositiveSmallIntegerField()
    encoding = models.CharField(max_length=50)


class ConditionAndReaction(models.Model):
    """Associate some criteria to the channel, in order to trigger an action
    (such as sending an email) in case one of these is satisfied.

    Examples of conditions:
    field1 _is_less_than_                X
    field2 _is_greater_or_equal_to_      X
    field1 _is_in_the_range_between_     (value1 and value2)
    field1 _is_out_of_the_range_between_ (value1 and value2)

    Valid arythmetic operations are the ones present in the Python stdlib:
    https://docs.python.org/3/library/operator.html
    * lt: less than
    * le: less than or equal
    * eq: equal
    * ne: not equal/different from
    * gt: greather than
    * ge: greather than or equal

    Moreover, some other arithmetic operators are provided.
    Note that for these two operations, the boundaries are not included (to
     avoid redundancy): to check also the boundaries, create more Conditions
     linked to the channel.
    * bt: between (the two limits)
    * ot: out (of the two limits)

    Some operators are provided for fields with string values:
    * cn: contains
    * nc: doesn't contain
    * sw: starts with
    * ew: ends with
    * eq: is equal
    * ne: isn't equal/is different from
    """

    # FIXME: implement all the checks to validate user's input.

    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    condition_op = models.CharField(max_length=2)
    value = models.CharField(max_length=20)

    # The field (of the record) on which the condition reacts on.
    # TODO: connect this to the fields of the channel.
    field_no = models.PositiveSmallIntegerField()
    # The second value has to be filled (in the forms) only for `bt' or `ot'.
    value_optional = models.CharField(max_length=20, null=True, blank=True)

    # Store the action the user choose to perform if the condition is met.
    action = models.CharField(max_length=10)

    def check_condition(self, field_obj):

        if field_obj.field_no != self.field_no:
            return False

        if self.condition_op == "lt":
            return op.lt(field_obj.value, self.value)
        elif self.condition_op == "le":
            return op.le(field_obj.value, self.value)
        elif self.condition_op == "eq":
            return op.eq(field_obj.value, self.value)
        elif self.condition_op == "ne":
            return op.ne(field_obj.value, self.value)
        elif self.condition_op == "gt":
            return op.gt(field_obj.value, self.value)
        elif self.condition_op == "ge":
            return op.ge(field_obj.value, self.value)

        elif self.condition_op == "bt":
            return self.value < field_obj.value < self.value_optional
        elif self.condition_op == "ot":
            return not (self.value < field_obj.value < self.value_optional)

        # TODO: test correctness with str and bytes objects (py3).
        elif self.condition_op == "cn":
            return self.value in field_obj.value
        elif self.condition_op == "nc":
            return self.value not in field_obj.value
        elif self.condition_op == "sw":
            return field_obj.value.startswith(self.value)
        elif self.condition_op == "ew":
            return field_obj.value.endswith(self.value)
        # We can rely on eq and ne in the arithmetic section also for strings.

        # In case no operation is defined for the given condition_op string:
        raise ValueError("No conditional operation is defined for operation "
                         "'{}'.".format(self.condition_op))

    def react(self, record_to_send):
        sentence = ("The following record, registered on: {}, verified one of"
                    " your conditions you set on channel {}.".format(
                        record_to_send,
                        self.channel)
                    )

        if self.action == "email":
            self.channel.send_email(message=sentence)

        # So far there are no other actions allowed to be executed.
        raise ValueError("No other actions allowed.")


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

    @property
    def real_value(self):
        encoding = self.record.channel.get_encoding(field_no=self.field_no)

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
                             "restore values at field no. {} of the channel"
                             " {}. Encoding proposed: '{}'; example of a value"
                             " saved: '{}'.".format(
                                 self.field_no,
                                 self.record.channel,
                                 encoding,
                                 self.value,
                             )
                             )
