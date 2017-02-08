from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views import generic

# from .models import Channel, User, Record, Field
from .models import *

import re

field_pattern = re.compile(r"(field[0-9]+)")
field_extract_number = re.compile(r"field([0-9]+)")
HTTP_WRITE_KEY = "X_SEST_Write_Key"

messages = {
    "MSG_NUMBER_FIELDS_EXCEEDED": "Max number of fields exceeded.",
    "MSG_WRONG_WRITE_KEY": "Incorrect SEST write key associated with the "
                           "channel you have chosen.",
    "MSG_MISSING_WRITE_KEY": "Missing writing API key.",
    "MSG_WRONG_HTTP_METHOD": "Only POST requests allowed.",
    "MSG_EMPTY_REQUEST": "Send at least one correct field inside your"
                         " message.",
}


class IndexView(generic.ListView):
    template_name = 'sest/index.html'
    context_object_name = 'latest_channels_edited'

    def get_queryset(self):
        return Channel.objects.all()


class ChannelView(generic.ListView):
    template_name = 'sest/channel.html'
    context_object_name = 'latest_records_added'

    n_elements_display = 10

    def get_queryset(self):
        r = Record.objects.order_by(
            '-insertion_time')[:self.n_elements_display]
        return r


def upload(request, channel_id):
    """View that analyses and performs some checks on an HTTP request
    submitted to a specific channel.

    Example of POST request:

        POST /12345678/upload HTTP/1.1
        Host: localhost
        Connection: close
        User-Agent: __whatever__
        X-Write-API-Key: e2af5d04-f62b-4fc6-ae50-049c3ecfaa18
        Content-Type: application/x-www-form-urlencoded
        Content-Length: 10

        field2=42


    Reference for the HTTP status codes
    https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
    """

    if request.method != "POST":
        return HttpResponseBadRequest(messages["MSG_WRONG_HTTP_METHOD"])

    write_API_key = request.META.get("HTTP_{}".format(HTTP_WRITE_KEY.upper()))

    if not write_API_key:
        return HttpResponseBadRequest(messages["MSG_MISSING_WRITE_KEY"])

    channel = get_object_or_404(Channel, pk=channel_id)

    if str(channel.write_key) != write_API_key:
        return HttpResponseBadRequest(messages["MSG_WRONG_WRITE_KEY"])

    # Collect the fields value from the body of the http POST message into a
    # dictionary. Use a regex to select only the fields like 'field<number>'.
    fields = {k: v for (k, v) in request.POST.items()
              if field_pattern.match(k)}

    if len(fields) > Channel.MAX_NUMBER_FIELDS:
        return HttpResponse(messages["MSG_NUMBER_FIELDS_EXCEEDED"], status=406)

    elif any(fields):
        # The object has to be created before attaching fields objects to it.
        r = Record.objects.create(channel=channel)

        # Create new Field objects to link to the newly created record.
        for field_name, val in fields.items():
            # Store in the db only the fields with a value.
            # TODO: check whether this is useful. R9.
            if not val:
                continue

            # Extract the field number and pass it to create the field element.
            # We can select just the first occurrence since we already
            # previously parsed the fields with another regex.
            # This allows to keep track of the "position" of the field passed
            # in the upload request.
            # extract number from: `field(123)'
            field_no = field_extract_number.findall(field_name)[0]
            field_no = int(field_no)
            field_no = int(field_no)

            r.field_set.create(field_no=field_no, val=val)

        # Save the object again with the new fields added, in order to possibly
        # trigger an action.
        r.save()
        return HttpResponse()

    else:
        return HttpResponse(messages["MSG_EMPTY_REQUEST"], status=406)
