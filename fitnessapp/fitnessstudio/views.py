from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Class
from .serializer import ClassSerializer


# Create your views here.

@api_view(['GET'])
def dashboard(request):
    all_classes = Class.objects.all()
    classes_serializer = ClassSerializer(all_classes, many=True)
    return Response({'classes': classes_serializer.data})