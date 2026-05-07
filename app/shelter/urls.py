from django.urls import path

from shelter.views import shelter_dashboard


urlpatterns = [
    path("", shelter_dashboard, name="shelter_dashboard"),
]