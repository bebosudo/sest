from django.test import TestCase, Client
from django.utils import timezone
from django.conf import settings
from django.core import mail

from .models import *

import uuid
# import postmarker
# from postmarker.core import PostmarkClient
import smtplib

POSTMARK_API_TEST = "POSTMARK_API_TEST"
# postmark_client_test = PostmarkClient(token=POSTMARK_API_TEST)


class UploadView(TestCase):

    def setUp(self):
        self.client = Client()
        self.u = User.objects.create(nick="test",
                                     registration_time=timezone.now())
        self.ch = Channel.objects.create(user=self.u,
                                         last_update=timezone.now(),
                                         number_fields=2
                                         )
        self.channel_uuid = str(self.ch.write_key)
        self.d = {'field2': 45}

    def test_upload_successful(self):
        """Use a POST http (made with the Client class from the test module) to
        test the correct upload of data to a channel, using the view `upload'.
        """

        response = self.client.post('/{}/upload/'.format(self.ch.id), self.d,
                                    HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(self.ch.record_set.all()[
                         0].field_set.count(), len(self.d))
        self.assertEqual(response.status_code, 200)

    def test_upload_exceeds_no_fields(self):
        """Use a POST http (made with the Client class from the test module) to
        check that we are not allowed to post more fields than the max number
        available.
        """

        self.d = {'field{}'.format(i + 1): i +
                  1 for i in range(Channel.MAX_NUMBER_FIELDS + 2)}
        response = self.client.post('/{}/upload/'.format(self.ch.id), self.d,
                                    HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(response.status_code, 406)

    def test_upload_zero_no_fields(self):
        """Use a POST http (made with the Client class from the test module) to
        make sure that user has to publish at least one field.
        """

        self.d = {}
        response = self.client.post('/{}/upload/'.format(self.ch.id), self.d,
                                    HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(response.status_code, 406)

    def test_upload_wrong_write_API(self):
        """Use a POST http (made with the Client class from the test module) to
        make sure that the view exits with a 400 Bad Request code in case the
        write API key provided is not the same as the one of the channel.
        """

        self.channel_uuid = uuid.uuid4()

        response = self.client.post('/{}/upload/'.format(self.ch.id), self.d,
                                    HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(response.status_code, 400)

    def test_upload_missing_write_API(self):
        """Use a POST http (made with the Client class from the test module) to
        make sure that the view exits with a 400 Bad Request code in case the
        write API key is provided.
        """

        response = self.client.post('/{}/upload/'.format(self.ch.id), self.d)
        #                             HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(response.status_code, 400)

    def test_upload_wrong_HTTP_request(self):
        """Use a POST http (made with the Client class from the test module) to
        make sure that the view exits with a 400 Bad Request code in case the
        write API key is provided.
        """

        # response = self.client.post('/{}/upload/'.format(self.ch.id), d)
        response = self.client.get('/{}/upload/'.format(self.ch.id), self.d,
                                   HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(response.status_code, 400)

##############################################################################


class FieldEncoding(TestCase):

    def setUp(self):
        self.client = Client()
        self.u = User.objects.create(nick="test")
                                     # registration_time=timezone.now())
        self.ch = Channel.objects.create(user=self.u,
                                         # last_update=timezone.now(),
                                         number_fields=2
                                         )
        self.channel_uuid = str(self.ch.write_key)
        self.ch.fieldencoding_set.create(field_no=1, encoding="float")
        self.ch.fieldencoding_set.create(field_no=2, encoding="float")
        self.d = {'field2': 3.141592}

    def test_fields_correct(self):
        """Create a new record and test the number and values of fields saved.
        """

        self.client.post('/{}/upload/'.format(self.ch.id), self.d,
                         HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        # r contains the record object just created.
        r = self.ch.record_set.all()[0]
        self.assertEqual(r.field_set.count(), len(self.d))

        self.assertEqual(r.field_set.all()[0].val, self.d['field2'])

    def test_field_encoding_no_operation_defined(self):
        """Create a new record, but set a wrong encoding in the channel.

        This should never happen, since the user should choose an encoding (
        boolean, int, float, etc) from a list with pre-defined objects.
        """

        # Wrong encoding set here.
        fe = self.ch.fieldencoding_set.get(field_no=2)
        fe.encoding = "asdf"
        fe.save()

        self.client.post('/{}/upload/'.format(self.ch.id), self.d,
                         HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        # r contains the record object just created.
        r = self.ch.record_set.all()[0]

        with self.assertRaises(ValueError):
            r.field_set.all()[0].val

    def test_field_encoding_wrong_value_saved(self):
        """Create a new record with a wrong value.

        This should never happen, since the values should be checked for
        consistency right before saving them in the DB.
        """

        self.d = {'field2': 'asdf'}
        self.client.post('/{}/upload/'.format(self.ch.id), self.d,
                         HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        # r contains the record object just created.
        r = self.ch.record_set.all()[0]

        with self.assertRaises(ValueError):
            r.field_set.all()[0].val

##############################################################################


class EmailSending(TestCase):

    def setUp(self):
        self.client = Client()
        self.u = User.objects.create(nick="test",
                                     registration_time=timezone.now())
        self.ch = Channel.objects.create(user=self.u,
                                         last_update=timezone.now(),
                                         number_fields=2
                                         )
        self.channel_uuid = str(self.ch.write_key)

    def test_send_email_successfully(self):

        e = self.u.notificationemail_set.create(
            address=settings.DEFAULT_FROM_EMAIL)
        self.ch.notification_email = e

        self.ch.send_email("test message")

        self.assertEqual(len(mail.outbox), 1)

    def test_send_email_wrong_recipient(self):

        e = self.u.notificationemail_set.create(address="")
        self.ch.notification_email = e

        # Uses Postmarker exception ATM. Create more tests for other services.
        # as cl_err:
        # with self.assertRaises(smtplib.SMTPRecipientsRefused) as e:
        # with self.assertRaises(postmarker.exceptions.ClientError):
        self.ch.send_email("test message")

        self.assertEqual(len(mail.outbox), 0)

        # TODO: Inspect the context manager and make sure that the exception
        # raised matches the error being tested.
