# Tests with boolean reactions, that simply return True whether an action
# has to be triggered.

from django.test import TestCase, Client
from django.utils import timezone
from django.conf import settings

from .models import *

# import uuid
# import postmarker
from postmarker.core import PostmarkClient

POSTMARK_API_TEST = "POSTMARK_API_TEST"
postmark_client_test = PostmarkClient(token=POSTMARK_API_TEST)


class Reactions(TestCase):

    def setUp(self):
        self.client = Client()
        self.u = User.objects.create(nick="test",
                                     registration_time=timezone.now())
        self.ch = Channel.objects.create(user=self.u,
                                         last_update=timezone.now(),
                                         number_fields=2
                                         )

        self.ch.fieldencoding_set.create(field_no=1, encoding="float")
        self.ch.fieldencoding_set.create(field_no=2, encoding="float")

        self.channel_uuid = str(self.ch.write_key)
        self.d = {'field2': 3.141592}

        settings.POSTMARK_CLIENT = postmark_client_test

        recipient = self.u.notificationemail_set.create(
            address=settings.DEFAULT_FROM_EMAIL)
        self.ch.notification_email = recipient

    def test_react_with_boolean_passing_lt(self):

        # Link a reaction (to be satisfied) to the channel.
        self.ch.conditionandreaction_set.create(condition_op="lt",
                                                field_no=2,
                                                val=10,
                                                action="test"
                                                )

        self.client.post('/{}/upload/'.format(self.ch.id), self.d,
                         HTTP_X_WRITE_API_KEY=self.channel_uuid)

        # The whole channel has been just created, so the last record created
        # is the only one present.
        r = Record.objects.all()[0]
        status = self.ch.check_and_react(r)

        self.assertEqual(status, True)

    def test_react_with_boolean_passing_le_equal(self):

        # Link a reaction (to be satisfied) to the channel.
        self.ch.conditionandreaction_set.create(condition_op="le",
                                                field_no=2,
                                                val=3.141592,
                                                action="test"
                                                )

        self.client.post('/{}/upload/'.format(self.ch.id), self.d,
                         HTTP_X_WRITE_API_KEY=self.channel_uuid)

        # The whole channel has been just created, so the last record created
        # is the only one present.
        r = Record.objects.all()[0]
        status = self.ch.check_and_react(r)

        self.assertEqual(status, True)

    def test_react_with_boolean_passing_le(self):

        # Link a reaction (to be satisfied) to the channel.
        self.ch.conditionandreaction_set.create(condition_op="le",
                                                field_no=2,
                                                val=10,
                                                action="test"
                                                )

        self.client.post('/{}/upload/'.format(self.ch.id), self.d,
                         HTTP_X_WRITE_API_KEY=self.channel_uuid)

        # The whole channel has been just created, so the last record created
        # is the only one present.
        r = Record.objects.all()[0]
        status = self.ch.check_and_react(r)

        self.assertEqual(status, True)

    def test_react_with_boolean_passing_eq(self):

        # Link a reaction (to be satisfied) to the channel.
        self.ch.conditionandreaction_set.create(condition_op="eq",
                                                field_no=2,
                                                val=3.141592,
                                                action="test"
                                                )

        self.client.post('/{}/upload/'.format(self.ch.id), self.d,
                         HTTP_X_WRITE_API_KEY=self.channel_uuid)

        # The whole channel has been just created, so the last record created
        # is the only one present.
        r = Record.objects.all()[0]
        status = self.ch.check_and_react(r)

        self.assertEqual(status, True)
