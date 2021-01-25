from rest_framework import serializers

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
    detail = serializers.HyperlinkedIdentityField(
        read_only=True,
        view_name='api:cars:car-detail', lookup_field='pk')

    class Meta:
        model = models.Car
        fields = ('id', 'brand', 'model', 'version', 'min_sale_value', 'detail')
