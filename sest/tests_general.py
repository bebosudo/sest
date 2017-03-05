from django.test import TestCase, Client
from django.conf import settings
from django.core import mail

from .models import *
from .views import messages

import uuid


class UploadView(TestCase):

    def setUp(self):
        self.client = Client()
        self.u = User.objects.create(username="test")
        self.ch = Channel.objects.create(user=self.u,
                                         number_fields=2
                                         )
        self.channel_uuid = str(self.ch.write_key)
        self.ch.fieldencoding_set.create(field_no=1, encoding="float")
        self.ch.fieldencoding_set.create(field_no=2, encoding="float")
        self.d = {"field2": 45}

    def test_upload_successful(self):
        """Use a POST http (made with the Client class from the test module) to
        test the correct upload of data to a channel, using the view `upload'.
        """

        response = self.client.post("/{}/".format(self.ch.id), self.d,
                                    HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(self.ch.record_set.all()[0].field_set.count(),
                         len(self.d))
        self.assertEqual(response.status_code, 200)

    def test_upload_exceeding_no_fields(self):
        """Use a POST http (made with the Client class from the test module) to
        check that we are not allowed to post more fields than the max number
        available.
        """

        self.d = {"field{}".format(i + 1): i + 1
                  for i in range(Channel.MAX_NUMBER_FIELDS + 2)}
        response = self.client.post("/{}/".format(self.ch.id), self.d,
                                    HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode("utf-8"),
                         messages["NUMBER_FIELDS_EXCEEDED"])

    def test_upload_wrong_write_API(self):
        """Use a POST http (made with the Client class from the test module) to
        make sure that the view exits with a 400 Bad Request code in case the
        write API key provided is not the same as the one of the channel.
        """

        self.channel_uuid = uuid.uuid4()

        response = self.client.post("/{}/".format(self.ch.id), self.d,
                                    HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode("utf-8"),
                         messages["WRONG_WRITE_KEY"])

    def test_upload_missing_write_API(self):
        """Use a POST http (made with the Client class from the test module) to
        make sure that the view exits with a 400 Bad Request code in case the
        write API key is provided.
        """

        response = self.client.post("/{}/".format(self.ch.id), self.d)
        #                             HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode("utf-8"),
                         messages["MISSING_WRITE_KEY"])

    def test_upload_wrong_HTTP_request(self):
        """Use a HEAD method (since the view is used for both GET and POST
        requests) to make sure that the view exits with a 400 Bad Request code.
        """

        # response = self.client.post(...)
        # response = self.client.get(...)
        response = self.client.get("/{}/".format(self.ch.id), self.d,
                                   HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(response.status_code, 400)
        # I don't know
        self.assertEqual(response.content.decode("utf-8"),
                         messages["WRONG_HTTP_METHOD"])

    def test_upload_empty_record_object(self):
        """Use a POST http (made with the Client class from the test module) to
        make sure that the user publishes all the fields with the correct
        names.
        """

        self.d = {}
        response = self.client.post("/{}/".format(self.ch.id), self.d,
                                    HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode("utf-8"),
                         messages["WRONG_FIELDS_PASSED"])

    def test_upload_record_one_key_wrong(self):
        """Refuse to save an object with a wrong key name out of two."""

        self.d.update({"field__number_missing__": 3.141592})
        response = self.client.post("/{}/".format(self.ch.id), self.d,
                                    HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode("utf-8"),
                         messages["WRONG_FIELDS_PASSED"])

    def test_upload_record_all_keys_wrong(self):
        """Refuse to save an object with all key names wrong."""

        self.d = {"field__number_missing__": 3.141592,
                  "field__here_as_well__": 3.141592}

        response = self.client.post("/{}/".format(self.ch.id), self.d,
                                    HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode("utf-8"),
                         messages["WRONG_FIELDS_PASSED"])

    def test_upload_field_with_empty_values(self):
        """In case there's at least one field with an empty value, exit with an
        error.
        Perform the needed cleanup of data partially saved in the DB during the
        process of uploading before discovering the empty value field.
        """

        self.d["field3"] = ""

        response = self.client.post("/{}/".format(self.ch.id), self.d,
                                    HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode("utf-8"),
                         messages["EMPTY_VALUES_NOT_ALLOWED"])
        self.assertEqual(Field.objects.count(), 0)
        self.assertEqual(Record.objects.count(), 0)

    def test_upload_field_wrong_value_encoding(self):
        """Refuse to save a field with a value that isn't coherent with the
        FieldEncoding associated with that specific field_no.
        """

        self.d["field2"] = "asdf"

        response = self.client.post("/{}/".format(self.ch.id), self.d,
                                    HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode("utf-8"),
                         messages["WRONG_VALUE_FIELD_ENCODING"])
        self.assertEqual(Field.objects.count(), 0)
        self.assertEqual(Record.objects.count(), 0)

    def test_upload_no_field_encoding_defined(self):
        """Refuse to save a record that tries to save a field that doesn't have
        an associated FieldEncoding object linked at the channel.
        """

        self.ch.fieldencoding_set.get(field_no=2).delete()

        response = self.client.post("/{}/".format(self.ch.id), self.d,
                                    HTTP_X_SEST_WRITE_KEY=self.channel_uuid)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode("utf-8"),
                         messages["WRONG_VALUE_FIELD_ENCODING"])
        self.assertEqual(Field.objects.count(), 0)
        self.assertEqual(Record.objects.count(), 0)


##############################################################################


class EmailSendingGeneral(TestCase):

    def setUp(self):
        self.client = Client()
        self.u = User.objects.create(username="test")
        self.ch = Channel.objects.create(user=self.u,
                                         number_fields=2
                                         )
        self.channel_uuid = str(self.ch.write_key)

    def test_send_email_successfully(self):

        e = self.u.notificationemail_set.create(
            address=settings.DEFAULT_FROM_EMAIL)
        self.ch.notification_email = e

        self.ch.send_email("test message")

        self.assertEqual(len(mail.outbox), 1)

    def tes_t_send_email_wrong_recipient(self):
        """In a real case scenario, an email sent to a wrong recipient should
        not be sent, but in a testing environment it passes without
        complaining.
        """

        e = self.u.notificationemail_set.create(address="asdf#sdf")
        self.ch.notification_email = e

        # with self.assertRaises(smtplib.SMTPRecipientsRefused) as e:
        # with self.assertRaises(postmarker.exceptions.ClientError):
        self.ch.send_email("test message")

        self.assertEqual(len(mail.outbox), 0)
