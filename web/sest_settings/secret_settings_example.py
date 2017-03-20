# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "asdfasdfasdfasfasdfasfasdfasdfasdfasdfasdfasdfasdf"

POSTMARK = {
    "TOKEN": "XXXXXXXX-YYYY-WWWW-VVVV-ZZZZZZZZZZZZ",
    "TEST_MODE": False,
}

# This is the default email for the whole django platform.
# It has to be set according to the 'trusted-senders' in the postmark settings.
DEFAULT_FROM_EMAIL = "user@example.com"

# Set the email of the admin that will receive a notification email in case of
# code errors when DEBUG=False
ADMINS = (("admin_name", "admin@example.com"), )
