from rest_framework import serializers
from .models import Image

class ImageUploadSerializer(serializers.ModelSerializer):
    # Optionally, include a method to get the full URL of the image
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = '__all__'

    def get_image_url(self, obj):
        return obj.image.url  
