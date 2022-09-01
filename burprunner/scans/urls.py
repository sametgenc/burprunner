from scans.views import ScansView
from django.urls import path


urlpatterns = [
    path("scans/<int:jenkins_id>", ScansView.as_view()),
]
