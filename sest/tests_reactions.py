# Tests with boolean reactions, that simply return True whether an action
# has to be triggered.

from django.test import TestCase, Client


class Reactions(TestCase):

    def test_react_with_boolean_passing_lt(self):

        settings.POSTMARK_CLIENT = postmark_client_test
        c, u, ch = create_testclient_user_channel()

        recipient = u.notificationemail_set.create(
            address=settings.DEFAULT_FROM_EMAIL)
        ch.notification_email = recipient

        ch_id = ch.id
        ch.fieldencoding_set.create(field_no=1, encoding="float")
        ch.fieldencoding_set.create(field_no=2, encoding="float")

        # Link a reaction (to be satisfied) to the channel.
        ch.conditionandreaction_set.create(condition_op="lt",
                                           field_no=2,
                                           val=10,
                                           action="test"
                                           )

        channel_uuid = str(ch.write_key)
        d = {'field2': 3.141592}
        c.post('/{}/upload/'.format(ch_id), d,
               HTTP_X_WRITE_API_KEY=channel_uuid)

        # The whole channel has been just created, so the last record created
        # is the only one present.
        r = Record.objects.all()[0]
        status = ch.check_and_react(r)

        self.assertEqual(status, True)

    def test_react_with_boolean_passing_le(self):

        settings.POSTMARK_CLIENT = postmark_client_test
        c, u, ch = create_testclient_user_channel()

        recipient = u.notificationemail_set.create(
            address=settings.DEFAULT_FROM_EMAIL)
        ch.notification_email = recipient

        ch_id = ch.id
        ch.fieldencoding_set.create(field_no=1, encoding="float")
        ch.fieldencoding_set.create(field_no=2, encoding="float")

        # Link a reaction (to be satisfied) to the channel.
        ch.conditionandreaction_set.create(condition_op="le",
                                           field_no=2,
                                           val=3.141592,
                                           action="test"
                                           )

        channel_uuid = str(ch.write_key)
        d = {'field2': 3.141592}
        c.post('/{}/upload/'.format(ch_id), d,
               HTTP_X_WRITE_API_KEY=channel_uuid)

        # The whole channel has been just created, so the last record created
        # is the only one present.
        r = Record.objects.all()[0]
        status = ch.check_and_react(r)

        self.assertEqual(status, True)

    def test_react_with_boolean_passing_le(self):

        settings.POSTMARK_CLIENT = postmark_client_test
        c, u, ch = create_testclient_user_channel()

        recipient = u.notificationemail_set.create(
            address=settings.DEFAULT_FROM_EMAIL)
        ch.notification_email = recipient

        ch_id = ch.id
        ch.fieldencoding_set.create(field_no=1, encoding="float")
        ch.fieldencoding_set.create(field_no=2, encoding="float")

        # Link a reaction (to be satisfied) to the channel.
        ch.conditionandreaction_set.create(condition_op="le",
                                           field_no=2,
                                           val=10,
                                           action="test"
                                           )

        channel_uuid = str(ch.write_key)
        d = {'field2': 3.141592}
        c.post('/{}/upload/'.format(ch_id), d,
               HTTP_X_WRITE_API_KEY=channel_uuid)

        # The whole channel has been just created, so the last record created
        # is the only one present.
        r = Record.objects.all()[0]
        status = ch.check_and_react(r)

        self.assertEqual(status, True)

    def test_react_with_boolean_passing_eq(self):

        settings.POSTMARK_CLIENT = postmark_client_test
        c, u, ch = create_testclient_user_channel()

        recipient = u.notificationemail_set.create(
            address=settings.DEFAULT_FROM_EMAIL)
        ch.notification_email = recipient

        ch_id = ch.id
        ch.fieldencoding_set.create(field_no=1, encoding="float")
        ch.fieldencoding_set.create(field_no=2, encoding="float")

        # Link a reaction (to be satisfied) to the channel.
        ch.conditionandreaction_set.create(condition_op="lt",
                                           field_no=2,
                                           val=3.141592,
                                           action="test"
                                           )

        channel_uuid = str(ch.write_key)
        d = {'field2': 3.141592}
        c.post('/{}/upload/'.format(ch_id), d,
               HTTP_X_WRITE_API_KEY=channel_uuid)

        # The whole channel has been just created, so the last record created
        # is the only one present.
        r = Record.objects.all()[0]
        status = ch.check_and_react(r)

        self.assertEqual(status, True)

    def test_react_with_boolean_passing_lt(self):

        settings.POSTMARK_CLIENT = postmark_client_test
        c, u, ch = create_testclient_user_channel()

        recipient = u.notificationemail_set.create(
            address=settings.DEFAULT_FROM_EMAIL)
        ch.notification_email = recipient

        ch_id = ch.id
        ch.fieldencoding_set.create(field_no=1, encoding="float")
        ch.fieldencoding_set.create(field_no=2, encoding="float")

        # Link a reaction (to be satisfied) to the channel.
        ch.conditionandreaction_set.create(condition_op="lt",
                                           field_no=2,
                                           val=10,
                                           action="test"
                                           )

        channel_uuid = str(ch.write_key)
        d = {'field2': 3.141592}
        c.post('/{}/upload/'.format(ch_id), d,
               HTTP_X_WRITE_API_KEY=channel_uuid)

        # The whole channel has been just created, so the last record created
        # is the only one present.
        r = Record.objects.all()[0]
        status = ch.check_and_react(r)

        self.assertEqual(status, True)

    def test_react_with_boolean_passing_lt(self):

        settings.POSTMARK_CLIENT = postmark_client_test
        c, u, ch = create_testclient_user_channel()

        recipient = u.notificationemail_set.create(
            address=settings.DEFAULT_FROM_EMAIL)
        ch.notification_email = recipient

        ch_id = ch.id
        ch.fieldencoding_set.create(field_no=1, encoding="float")
        ch.fieldencoding_set.create(field_no=2, encoding="float")

        # Link a reaction (to be satisfied) to the channel.
        ch.conditionandreaction_set.create(condition_op="lt",
                                           field_no=2,
                                           val=10,
                                           action="test"
                                           )

        channel_uuid = str(ch.write_key)
        d = {'field2': 3.141592}
        c.post('/{}/upload/'.format(ch_id), d,
               HTTP_X_WRITE_API_KEY=channel_uuid)

        # The whole channel has been just created, so the last record created
        # is the only one present.
        r = Record.objects.all()[0]
        status = ch.check_and_react(r)

        self.assertEqual(status, True)

    def test_react_with_boolean_passing_lt(self):

        settings.POSTMARK_CLIENT = postmark_client_test
        c, u, ch = create_testclient_user_channel()

        recipient = u.notificationemail_set.create(
            address=settings.DEFAULT_FROM_EMAIL)
        ch.notification_email = recipient

        ch_id = ch.id
        ch.fieldencoding_set.create(field_no=1, encoding="float")
        ch.fieldencoding_set.create(field_no=2, encoding="float")

        # Link a reaction (to be satisfied) to the channel.
        ch.conditionandreaction_set.create(condition_op="lt",
                                           field_no=2,
                                           val=10,
                                           action="test"
                                           )

        channel_uuid = str(ch.write_key)
        d = {'field2': 3.141592}
        c.post('/{}/upload/'.format(ch_id), d,
               HTTP_X_WRITE_API_KEY=channel_uuid)

        # The whole channel has been just created, so the last record created
        # is the only one present.
        r = Record.objects.all()[0]
        status = ch.check_and_react(r)

        self.assertEqual(status, True)

    def test_react_with_boolean_passing_lt(self):

        settings.POSTMARK_CLIENT = postmark_client_test
        c, u, ch = create_testclient_user_channel()

        recipient = u.notificationemail_set.create(
            address=settings.DEFAULT_FROM_EMAIL)
        ch.notification_email = recipient

        ch_id = ch.id
        ch.fieldencoding_set.create(field_no=1, encoding="float")
        ch.fieldencoding_set.create(field_no=2, encoding="float")

        # Link a reaction (to be satisfied) to the channel.
        ch.conditionandreaction_set.create(condition_op="lt",
                                           field_no=2,
                                           val=10,
                                           action="test"
                                           )

        channel_uuid = str(ch.write_key)
        d = {'field2': 3.141592}
        c.post('/{}/upload/'.format(ch_id), d,
               HTTP_X_WRITE_API_KEY=channel_uuid)

        # The whole channel has been just created, so the last record created
        # is the only one present.
        r = Record.objects.all()[0]
        status = ch.check_and_react(r)

        self.assertEqual(status, True)

    def test_react_with_boolean_passing_lt(self):

        settings.POSTMARK_CLIENT = postmark_client_test
        c, u, ch = create_testclient_user_channel()

        recipient = u.notificationemail_set.create(
            address=settings.DEFAULT_FROM_EMAIL)
        ch.notification_email = recipient

        ch_id = ch.id
        ch.fieldencoding_set.create(field_no=1, encoding="float")
        ch.fieldencoding_set.create(field_no=2, encoding="float")

        # Link a reaction (to be satisfied) to the channel.
        ch.conditionandreaction_set.create(condition_op="lt",
                                           field_no=2,
                                           val=10,
                                           action="test"
                                           )

        channel_uuid = str(ch.write_key)
        d = {'field2': 3.141592}
        c.post('/{}/upload/'.format(ch_id), d,
               HTTP_X_WRITE_API_KEY=channel_uuid)

        # The whole channel has been just created, so the last record created
        # is the only one present.
        r = Record.objects.all()[0]
        status = ch.check_and_react(r)

        self.assertEqual(status, True)
