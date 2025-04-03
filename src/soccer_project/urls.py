from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from soccer_project.api import views

urlpatterns = [
    path("", views.api_root, name="api-root"),  # Homepage
    path("play/", views.MatchView.as_view(), name="play_match"),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
