from django.test import TestCase, Client
from django.conf import settings
from django.core import mail

from .models import *


class Reactions(TestCase):

    def setUp(self):
        self.client = Client()
        self.u = User.objects.create(username="test")
        ne = NotificationEmail.objects.create(user=self.u,
                                              address="whatever@test.it")
        self.ch = Channel.objects.create(user=self.u,
                                         number_fields=2,
                                         notification_email=ne
                                         )

        self.ch.fieldmetadata_set.create(field_no=1, encoding="float")
        self.ch.fieldmetadata_set.create(field_no=2, encoding="float")

        self.channel_uuid = str(self.ch.write_key)
        self.d = {'field2': 3.141592}

        # settings.POSTMARK_CLIENT = postmark_client_test

        recipient = self.u.notificationemail_set.create(
            address=settings.DEFAULT_FROM_EMAIL)
        self.ch.notification_email = recipient

    ########################################
    # Create more tests for every condition.
    ########################################

    def test_react_with_email_not_triggering_any_action(self):

        # Link a reaction (NOT to be satisfied) to the channel.
        self.ch.conditionandreaction_set.create(condition_op="lt",
                                                field_no=2,
                                                val=2,
                                                action="email"
                                                )

        self.client.post('/{}/'.format(self.ch.id), self.d,
                         HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(len(mail.outbox), 0)

    def test_react_with_email_passing_lt_on_save(self):

        # Link a reaction (to be satisfied) to the channel.
        self.ch.conditionandreaction_set.create(condition_op="lt",
                                                field_no=2,
                                                val=10,
                                                action="email"
                                                )

        self.client.post('/{}/'.format(self.ch.id), self.d,
                         HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(len(mail.outbox), 1)

    def test_react_with_email_passing_bt_on_save(self):

        # Link a reaction (to be satisfied) to the channel.
        self.ch.conditionandreaction_set.create(condition_op="bt",
                                                field_no=2,
                                                val=0,
                                                val_opt=10,
                                                action="email"
                                                )

        self.client.post('/{}/'.format(self.ch.id), self.d,
                         HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(len(mail.outbox), 1)

    def test_react_with_email_passing_sw_on_save(self):
        fe = self.ch.fieldmetadata_set.get(field_no=2)
        fe.encoding = "string"
        fe.save()

        s = "test"
        # Link a reaction (to be satisfied) to the channel.
        self.ch.conditionandreaction_set.create(condition_op="sw",
                                                field_no=2,
                                                val=s,
                                                action="email"
                                                )

        self.d = {"field2": s + " and sth else.. etc etc"}
        self.client.post('/{}/'.format(self.ch.id), self.d,
                         HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(len(mail.outbox), 1)
