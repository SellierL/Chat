import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets

from cats.models import Owner, Cat
from cats.serializers import OwnerSerializer, CatSerializer
from shelter.models import ShelterCat


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all().order_by("id")
    serializer_class = OwnerSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.select_related("owner").all().order_by("id")
    serializer_class = CatSerializer


def home(request):
    owners = Owner.objects.prefetch_related("cats").all().order_by("id")
    cats = Cat.objects.select_related("owner").all().order_by("is_adopted", "id")
    shelter_cats = ShelterCat.objects.using("shelter").all().order_by("id")

    return render(
        request,
        "cats/home.html",
        {
            "owners": owners,
            "cats": cats,
            "shelter_cats": shelter_cats,
        },
    )

@login_required
def transfer_cat_to_shelter(request, cat_id):
    authorized_username = os.getenv("TRANSFER_AUTHORIZED_USERNAME")

    if request.user.username != authorized_username:
        messages.error(request, "Vous n'êtes pas autorisé à transférer ce chat.")
        return redirect("home")

    if request.method != "POST":
        messages.error(request, "Méthode non autorisée.")
        return redirect("home")

    cat = get_object_or_404(
        Cat.objects.select_related("owner"),
        id=cat_id,
    )

    if cat.is_adopted:
        messages.info(request, f"{cat.name} a déjà été adopté.")
        return redirect("home")

    ShelterCat.objects.using("shelter").update_or_create(
        source_cat_id=cat.id,
        defaults={
            "name": cat.name,
            "age": cat.age,
            "breed": cat.breed,
            "provenance": cat.provenance,
            "particularity": cat.particularity,
            "image_url": cat.image_url,
            "owner_name": cat.owner.first_name,
            "owner_email": cat.owner.email,
            "boarding_status": "adopted",
        },
    )

    cat.is_adopted = True
    cat.save(update_fields=["is_adopted"])

    messages.success(
        request,
        f"{cat.name} a été transféré vers la base du refuge."
    )

    return redirect("home")