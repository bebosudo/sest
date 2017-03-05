from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.conf import settings

from .models import *

import re

field_pattern = re.compile(r"(field[0-9]+)")
field_extract_number = re.compile(r"field([0-9]+)")
HTTP_WRITE_KEY = "X_SEST_Write_Key"

messages = {
    "NUMBER_FIELDS_EXCEEDED": "Max number of fields exceeded.",
    "WRONG_WRITE_KEY": ("Incorrect SEST write key associated with the "
                        "channel you have chosen."),
    "MISSING_WRITE_KEY": "Missing writing API key.",
    "WRONG_HTTP_METHOD": "Only GET and POST requests are allowed.",
    "WRONG_FIELDS_PASSED": "One or more fields sent have wrong names.",
    "WRONG_VALUE_FIELD_ENCODING": ("One of the value sent was not coherent "
                                   "with the encoding defined for the field "
                                   "number for the channel, or the channel is"
                                   "not defined to handle that field number."),
    "EMPTY_VALUES_NOT_ALLOWED": "Fields with empty values are not allowed."
}


class IndexView(generic.ListView):
    template_name = 'sest/index.html'
    context_object_name = 'latest_channels_edited'

    def get_queryset(self):
        return Channel.objects.order_by("-last_update")


# class ChannelView(generic.ListView):
#     template_name = 'sest/channel.html'
#     context_object_name = 'latest_records_added'

#     n_elements_display = 10

#     def get_queryset(self):
#         r = Record.objects.order_by(
#             '-insertion_time')[:self.n_elements_display]
#         return r

def channel(request, channel_id):
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

    How to choose HTTP response codes:
    http://racksburg.com/choosing-an-http-status-code/
    """

    channel = get_object_or_404(Channel, pk=channel_id)

    if request.method == "GET":
        n_elements_display = 10

        records_to_display = Record.objects.order_by(
            "-insertion_time")[:n_elements_display]

        records_to_display.field_names = channel.get_field_names()
        context = {"last_records_uploaded": records_to_display}
        return render(request, "sest/channel.html", context)

    elif request.method != "POST":
        return HttpResponseBadRequest(messages["WRONG_HTTP_METHOD"])
        # return HttpResponse(status=400, reason="dfs")

    write_API_key = request.META.get("HTTP_{}".format(HTTP_WRITE_KEY.upper()))

    if not write_API_key:
        return HttpResponseBadRequest(messages["MISSING_WRITE_KEY"])

    if str(channel.write_key) != write_API_key:
        return HttpResponseBadRequest(messages["WRONG_WRITE_KEY"])

    # Use a regex to select only the fields like 'field<number>'.
    fields = {k: v for (k, v) in request.POST.items()
              if field_pattern.match(k)}

    if len(fields) > settings.MAX_NUMBER_FIELDS:
        return HttpResponseBadRequest(messages["NUMBER_FIELDS_EXCEEDED"])

    elif len(fields) < len(request.POST.keys()):
        # This means that the user inserted at least one field with an
        # incorrect name.
        return HttpResponseBadRequest(messages["WRONG_FIELDS_PASSED"])

    elif any(fields):
        # The object has to be created before attaching fields objects to it.
        r = Record.objects.create(channel=channel)

        for field_name, val in fields.items():
            # 'field_name' and 'val' are strings like 'field2' and '3.5'.

            # Store in the db only the fields with a value. Clean up in case.
            if not val:
                r.delete()
                return HttpResponseBadRequest(
                    messages["EMPTY_VALUES_NOT_ALLOWED"]
                )

            # Extract the field number, to store it to the right position.
            field_no = field_extract_number.findall(field_name)[0]
            field_no = int(field_no)

            try:
                r.field_set.create(field_no=field_no, val=val)
            except ValueError:
                # A value with a wrong encoding (according to the associated
                # encoding in the FieldMetadata object on the field number) was
                # going to be saved.
                r.delete()
                return HttpResponseBadRequest(
                    messages["WRONG_VALUE_FIELD_ENCODING"]
                )

        # Save the object again with the new fields added, in order to possibly
        # trigger an action.
        r.save()
        return HttpResponse()

    else:
        # This means that the user tried to insert an empty record.
        return HttpResponseBadRequest(messages["WRONG_FIELDS_PASSED"])
