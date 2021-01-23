from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
