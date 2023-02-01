from rest_framework.serializers import ModelSerializer

from app_main.models import Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
