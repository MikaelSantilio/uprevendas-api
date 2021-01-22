from rest_framework import serializers

from up_revendas.cars import models


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Car
        fields = '__all__'


class ProffyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProffyUser
        fields = ['name', 'avatar', 'bio', 'whatsapp', 'id']


class ClassSerializer(serializers.ModelSerializer):
    proffy_user = ProffyUserSerializer()

    class Meta:
        model = models.Class
        fields = ['subject', 'cost', 'proffy_user']


class ClassScheduleSerializer(serializers.ModelSerializer):
    klass = ClassSerializer()

    class Meta:
        model = models.ClassSchedule
        fields = ['week_day', 'start_at', 'end_at', 'klass']


class ScheduleSerializer(serializers.Serializer):
    week_day = serializers.IntegerField(min_value=1, max_value=7)
    start_at = serializers.CharField(max_length=5)
    end_at = serializers.CharField(max_length=5)


class ClassSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=128)
    avatar = serializers.CharField(max_length=164)
    whatsapp = serializers.CharField(max_length=20)
    bio = serializers.CharField(max_length=256)
    subject = serializers.CharField(max_length=64)
    cost = serializers.DecimalField(max_digits=8, decimal_places=2)
    schedule = ScheduleSerializer(many=True)
