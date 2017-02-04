from django.conf import settings
from django.core.mail import send_mail
# pip install postmarker


def send_email_wrapper(recipients_list, subject,
                       from_field=settings.DEFAULT_FROM_EMAIL,
                       text_body=None, html_body=None):
    """Just a wrapper around different third-party services that send email.

    So far, I only pass the arguments from this function to another one, but
    I plan to introduce a smart system that takes into account the number of
    emails sent with each third-party service, in order to use free credits
    from many different services.
    """

    if not html_body and not text_body:
        raise TypeError("A html or a text body has to be provided.")

    if isinstance(recipients_list, str):
        recipients_list = [recipients_list]

    return send_email_postmark(from_field, recipients_list, subject,
                               text_body, html_body)


def send_email_postmark(from_field, to_list, subject,
                        text_body=None, html_body=None):
    """Postmark[app.com] API client.

    In order to use the postmark service, visit their website, register a
    (free) user, create a sending server, get its token (Credentials >
    Server API) and save it into settings.py. Then instantiate a PM Client
    object to be called from this function.
    """

    # if not client:
    #     client = settings.POSTMARK_CLIENT

    no_email_sent = send_mail(
        subject,
        # Text and Html bodies can be sent together into a multipart email.
        text_body,
        from_field,
        to_list,
        html_message=html_body,
        fail_silently=True,
    )

    return no_email_sent == len(to_list)
