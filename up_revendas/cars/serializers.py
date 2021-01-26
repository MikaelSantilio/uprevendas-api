from rest_framework import serializers
from django.urls import reverse
from up_revendas.cars import models


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Brand
        fields = ('id', 'name')


class ModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Model
        fields = ('id', 'brand', 'name')


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Car
        fields = (
            "id",
            "license_plate",
            "year",
            "version",
            "transmission",
            "mileage",
            "car_type",
            "color",
            "min_sale_value",
            "brand",
            "model")


class CarDetailSerializer(CarSerializer):
    brand = serializers.CharField(source='brand.name')
    model = serializers.CharField(source='model.name')


class CarHyperlinkSerializer(serializers.ModelSerializer):
    brand = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
     )
    model = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
     )
    links = serializers.SerializerMethodField()
    # detail = serializers.HyperlinkedIdentityField(
    #     read_only=True,
    #     view_name='api:cars:car-detail', lookup_field='pk')

    class Meta:
        model = models.Car
        fields = ('id', 'brand', 'model', 'version', 'min_sale_value', 'links')

    def get_links(self, obj):
        data = []

        request = self.context['request']

        data.append(
            {
                "type": "GET",
                "rel": "self",
                "uri": request.build_absolute_uri(
                    reverse("api:cars:cars-detail", kwargs={'pk': obj.id}))
            }
        )

        if request.user.is_authenticated:

            if request.user.is_store_manager or request.user.is_superuser:
                data += [
                    {
                        "type": "POST",
                        "rel": "create",
                        "uri": request.build_absolute_uri(reverse("api:cars:cars-list"))
                    },
                    {
                        "type": "PUT",
                        "rel": "update",
                        "uri": request.build_absolute_uri(reverse("api:cars:cars-detail", kwargs={'pk': obj.id}))
                    },
                    {
                        "type": "DELETE",
                        "rel": "update",
                        "uri": request.build_absolute_uri(reverse("api:cars:cars-detail", , kwargs={'pk': obj.id}))
                    }
                ]

        return data
