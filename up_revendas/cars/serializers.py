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
        fields = '__all__'


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
        view_name='api:car-detail', lookup_field='pk')

    class Meta:
        model = models.Car
        fields = ('brand', 'model', 'version', 'sale_value', 'detail')
