from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import viewsets

from shelter.models import ShelterCat
from shelter.serializers import ShelterCatSerializer


@login_required
def shelter_dashboard(request):
    shelter_cats = ShelterCat.objects.using("shelter").all().order_by("id")

    return render(
        request,
        "shelter/dashboard.html",
        {
            "shelter_cats": shelter_cats,
        },
    )


class ShelterCatViewSet(viewsets.ModelViewSet):
    serializer_class = ShelterCatSerializer

    def get_queryset(self):
        return ShelterCat.objects.using("shelter").all().order_by("id")