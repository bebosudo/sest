from postmarker.core import PostmarkClient

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'asdfasdfasdfasfasdfasfasdfasdfasdfasdfasdfasdfasdf'


POSTMARK_CLIENT = PostmarkClient(token="XXXXXXXX-YYYY-WWWW-VVVV-ZZZZZZZZZZZZ")

# This is the default email for the whole django platform.
DEFAULT_FROM_EMAIL = "user@example.com"
