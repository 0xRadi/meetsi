from django.contrib import admin
from jitsi.models import Meeting, Attendee


class AttendeeInline(admin.TabularInline):
    model = Attendee


class MeetingAdmin(admin.ModelAdmin):
    inlines = [AttendeeInline]
    list_display = ('room_id', 'subject', 'start_time', 'owner', 'is_anonymous')
    list_filter = ['start_time']
    search_fields = ['subject']


admin.site.register(Meeting, MeetingAdmin)
