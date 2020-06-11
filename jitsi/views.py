from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.http import JsonResponse
from django.conf import settings
from jitsi.models import Attendee, Meeting


# to require login uncomment @login_required

@login_required
def home(request):
    upcoming = Attendee.objects.filter(user=request.user, meeting__start_time__gt=timezone.now()).order_by('meeting__start_time')
    return render(request, 'jitsi/dashboard.html', {"upcoming": upcoming})


@login_required
def meeting_data(request, room):
    attendee = Attendee.objects.get(meeting__room_id=room, user=request.user)
    return JsonResponse({
        "jwt": attendee.jwt(),
        "roomName": attendee.meeting.room_id,
        "domain": settings.JITSI_DOMAIN,
        "subject": attendee.meeting.subject
    })


@login_required
def meeting(request, room):
    if not Attendee.objects.filter(user=request.user, meeting__room_id=room).exists():
        raise PermissionDenied
    meet = get_object_or_404(Meeting, room_id=room)
    attendees = meet.attendees.all()
    guest_link = None
    if meet.is_anonymous:
        guest_link = "https://{}/{}?jwt={}".format(settings.JITSI_DOMAIN, meet.room_id, meet.jwt())
    return render(request, 'jitsi/meeting.html', {"meeting": meet, "attendees": attendees, "guest_link": guest_link})
