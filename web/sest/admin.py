from django.contrib import admin

from .models import *


class ChannelInLine(admin.StackedInline):
    model = Channel
    extra = 1


class UserAdmin(admin.ModelAdmin):
    inlines = [ChannelInLine]


# There's no more need to add the User manually to the admin panel, since it's
# already provided by the django.contrib.auth module.
# admin.site.register(User, UserAdmin)

admin.site.register(Channel)
