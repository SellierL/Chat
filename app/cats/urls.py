from django.urls import include, path
from rest_framework.routers import DefaultRouter

from cats.views import OwnerViewSet, CatViewSet
from shelter.views import ShelterCatViewSet


router = DefaultRouter()
router.register(r"owners", OwnerViewSet, basename="owner")
router.register(r"cats", CatViewSet, basename="cat")
router.register(r"shelter-cats", ShelterCatViewSet, basename="shelter-cat")

urlpatterns = [
    path("", include(router.urls)),
]