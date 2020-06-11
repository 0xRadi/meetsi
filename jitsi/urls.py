from jitsi.views import home, meeting, meeting_data
from django.urls import path

urlpatterns = [
    path('meeting/<uuid:room>', meeting, name='meeting'),
    path('meeting/<uuid:room>/data', meeting_data, name='meeting_api'),
    path('', home, name="jitsi_home"),
]
