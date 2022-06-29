from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import DataObat
from .serializers import DataObatSerializer

class DataObatViewSet(viewsets.ModelViewSet):
    queryset = DataObat.objects.all().order_by('nama_obat')
    serializer_class = DataObatSerializer
    permission_classes = [permissions.IsAuthenticated]