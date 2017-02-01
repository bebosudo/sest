from django.contrib import admin

from .models import User, Channel, Record


class ChannelInLine(admin.StackedInline):
    model = Channel
    extra = 1

class UserAdmin(admin.ModelAdmin):
    inlines = [ChannelInLine]

admin.site.register(User, UserAdmin)
admin.site.register(Channel)
