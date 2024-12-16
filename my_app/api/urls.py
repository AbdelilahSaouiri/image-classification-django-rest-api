from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import image_classification,getImages,upload_image_by_admin

urlpatterns = [
    path('upload/', image_classification, name='image-upload'),
    path('images/', getImages, name='get-all-images'),
    path('admin/upload', upload_image_by_admin, name='upload_image_by_admin'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
