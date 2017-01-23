from django.test import TestCase, Client
# from django.test.utils import override_settings
from django.utils import timezone

from .models import User, Channel, Record

import uuid


class UploadView(TestCase):

    def test_upload_successful(self):
        """Use a POST http (made with the Client class from the test module) to
        test the correct upload of data to a channel, using the view `upload'.
        """

        c = Client()

        channel_id = 1234

        u = User.objects.create(nick="test", registration_time=timezone.now())
        ch = Channel.objects.create(user=u, id=channel_id, last_update=timezone.now())
        channel_uuid = str(ch.write_key)

        d = {'field2': 45}
        response = c.post('/{}/upload/'.format(channel_id), d,
                          HTTP_X_WRITE_API_KEY=channel_uuid)

        self.assertEqual(response.status_code, 200)

    def test_upload_exceeds_no_fields(self):
        """Use a POST http (made with the Client class from the test module) to
        check that we are not allowed to post more fields than the max number
        available.
        """

        c = Client()

        channel_id = 1234

        u = User.objects.create(nick="test", registration_time=timezone.now())
        ch = Channel.objects.create(user=u, id=channel_id, last_update=timezone.now())
        channel_uuid = str(ch.write_key)

        d = {'field{}'.format(i+1): i+1 for i in range(Record.MAX_NUMBER_FIELDS+2)}
        response = c.post('/{}/upload/'.format(channel_id), d,
                          HTTP_X_WRITE_API_KEY=channel_uuid)

        self.assertEqual(response.status_code, 406)

    def test_upload_zero_no_fields(self):
        """Use a POST http (made with the Client class from the test module) to
        make sure that user has to publish at least one field.
        """

        c = Client()

        channel_id = 1234

        u = User.objects.create(nick="test", registration_time=timezone.now())
        ch = Channel.objects.create(user=u, id=channel_id, last_update=timezone.now())
        channel_uuid = str(ch.write_key)

        d = {}
        response = c.post('/{}/upload/'.format(channel_id), d,
                          HTTP_X_WRITE_API_KEY=channel_uuid)

        self.assertEqual(response.status_code, 406)

    def test_upload_wrong_write_API(self):
        """Use a POST http (made with the Client class from the test module) to
        make sure that the view exits with a 400 Bad Request code in case the
        write API key provided is not the same as the one of the channel.
        """

        c = Client()

        channel_id = 1234

        u = User.objects.create(nick="test", registration_time=timezone.now())
        ch = Channel.objects.create(user=u, id=channel_id, last_update=timezone.now())
        channel_uuid = uuid.uuid4()

        d = {'field2': 45}
        response = c.post('/{}/upload/'.format(channel_id), d,
                          HTTP_X_WRITE_API_KEY=channel_uuid)

        self.assertEqual(response.status_code, 400)

    def test_upload_missing_write_API(self):
        """Use a POST http (made with the Client class from the test module) to
        make sure that the view exits with a 400 Bad Request code in case the
        write API key is provided.
        """

        c = Client()

        channel_id = 1234

        u = User.objects.create(nick="test", registration_time=timezone.now())
        ch = Channel.objects.create(user=u, id=channel_id, last_update=timezone.now())
        # channel_uuid = uuid.uuid4()

        d = {'field2': 45}
        response = c.post('/{}/upload/'.format(channel_id), d)
                          # HTTP_X_WRITE_API_KEY=channel_uuid)

        self.assertEqual(response.status_code, 400)

    def test_upload_wrong_HTTP_request(self):
        """Use a POST http (made with the Client class from the test module) to
        make sure that the view exits with a 400 Bad Request code in case the
        write API key is provided.
        """

        c = Client()

        channel_id = 1234

        u = User.objects.create(nick="test", registration_time=timezone.now())
        ch = Channel.objects.create(user=u, id=channel_id, last_update=timezone.now())
        # channel_uuid = uuid.uuid4()

        d = {'field2': 45}
        response = c.get('/{}/upload/'.format(channel_id), d)
                          # HTTP_X_WRITE_API_KEY=channel_uuid)

        self.assertEqual(response.status_code, 400)

