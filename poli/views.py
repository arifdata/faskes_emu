from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Diagnosa
from .serializers import DiagnosaSerializer

# Create your views here.
class DiagnosaViewSet(viewsets.ModelViewSet):
    queryset = Diagnosa.objects.all()
    serializer_class = DiagnosaSerializer
    permission_classes = [permissions.IsAuthenticated]