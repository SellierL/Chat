from rest_framework import serializers

from shelter.models import ShelterCat


class ShelterCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShelterCat
        fields = [
            "id",
            "source_cat_id",
            "name",
            "age",
            "breed",
            "provenance",
            "particularity",
            "image_url",
            "owner_name",
            "owner_email",
            "boarding_status",
            "adoption_date",
        ]