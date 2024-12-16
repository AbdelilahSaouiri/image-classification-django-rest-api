from tensorflow.keras.applications import EfficientNetB7
from tensorflow.keras.applications.efficientnet import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from rest_framework.pagination import PageNumberPagination 
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Image
import numpy as np
from .serializers import ImageUploadSerializer
import io


model = EfficientNetB7(weights='imagenet')

def classify_image(image_file):
    try:
        image_stream = io.BytesIO(image_file.read())
        img = load_img(image_stream, target_size=(600, 600))  
        x = img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        predictions = model.predict(x)
        return decode_predictions(predictions, top=3)[0]  # Top 3 résultats
    except Exception as e:
        raise ValueError(f"Erreur lors de la classification : {str(e)}")

def getTwinImageUrl(title):
    images = Image.objects.filter(title=title)
    if images.exists():
        return [image.image.url for image in images] 
    return []

@api_view(['POST'])
def image_classification(request):
    if 'image' not in request.FILES:
        return Response({"error": "Aucune image fournie"}, status=400)

    serializer = ImageUploadSerializer(data=request.FILES)
    if serializer.is_valid():
        image_file = request.FILES['image']

        try:
            
            predictions = classify_image(image_file)
            best_prediction = max(predictions, key=lambda x: x[2])  # Meilleure classe détectée
            
           
            urls_images = getTwinImageUrl(best_prediction[1])
            if urls_images:
                return Response({
                    "predictions": {
                        "description": best_prediction[1],
                        "score": float(best_prediction[2])
                    },
                    "image_urls": urls_images
                })
            
            return Response({"message": "Ce produit n'existe pas pour le moment."}, status=404)

        except ValueError as e:
            return Response({"error": str(e)}, status=500)

    return Response(serializer.errors, status=400)

@api_view(['GET'])
def getImages(request):
    images = Image.objects.all() 
    paginator = PageNumberPagination()
    paginator.page_size = 8
    paginated_pages = paginator.paginate_queryset(images, request)
    serializer = ImageUploadSerializer(paginated_pages, many=True)

    return paginator.get_paginated_response(serializer.data)

# upload image by admin

@api_view(['POST'])
def upload_image_by_admin(request):
    if 'image' not in request.FILES:
        return Response({"error": "Aucune image fournie"}, status=400)

    serializer = ImageUploadSerializer(data=request.FILES)
    if serializer.is_valid():
        image_file = request.FILES['image']


        predictions = classify_image(image_file)
        best_prediction = max(predictions, key=lambda x: x[2])  
        saved = serializer.save()
        saved.title = best_prediction[1]
        saved.save()

        return Response({"message": "Image enregistrée avec succès", "title": saved.title}, status=201)
            
    return Response({"message": "Erreur lors de l'enregistrement de l'image.", "errors": serializer.errors}, status=400)


