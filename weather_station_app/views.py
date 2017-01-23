from django.http import HttpResponse
from django.shortcuts import get_object_or_404  # , render
from django.utils import timezone
from django.views import generic

from .models import Channel, Record, Field

import re

field_pattern = re.compile(r"(field[0-9]+)")
HTTP_WRITE_KEY = "X_Write_API_Key"


class IndexView(generic.ListView):
    template_name = 'weather_station_app/index.html'
    context_object_name = 'latest_channels_edited'

    def get_queryset(self):
        return Channel.objects.all()


class ChannelView(generic.ListView):
    template_name = 'weather_station_app/channel.html'
    context_object_name = 'latest_records_added'

    n_elements_display = 10

    def get_queryset(self):
        return Record.objects.order_by('-insertion_time')[:self.n_elements_display]


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
    
    if request.method == "POST":
        write_API_key = request.META.get("HTTP_{}".format(HTTP_WRITE_KEY.upper()))

        if write_API_key:
            channel = get_object_or_404(Channel, pk=channel_id)

            if str(channel.write_key) == write_API_key:
                # Collect the fields value from the body of the http POST 
                # message into a dictionary.
                fields = {k: v for (k, v) in request.POST.items()
                               if field_pattern.match(k)}

                if len(fields) > Record.MAX_NUMBER_FIELDS:
                    return HttpResponse("Max number of fields exceeded.", status=406)

                elif any(fields):
                    r = Record.objects.create(channel=channel,
                                              insertion_time=timezone.now() )

                    # Create new Field objects to link to the newly created record.
                    for i, k in enumerate(fields):
                        val = fields[k]
                        # Store in the db only the fields with a value.
                        if not val:
                            continue

                        # Shift the field counter by 1, since enumerate starts from 0.
                        i += 1
                        Field.objects.create(record=r, field_no=i, value=val)

                        return HttpResponse(status=200)

                else:
                    return HttpResponse("Send at least one field inside your "
                                        "message.", status=406)
            else:
                return HttpResponse("Incorrect API key associated with the "
                             "channel you have chosen.", status=400)
        else:
            return HttpResponse("Missing writing API key.", status=400)
    else:
        return HttpResponse("Only POST requests allowed.", status=400)
