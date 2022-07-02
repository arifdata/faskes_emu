from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import DataObat, BukuPenerimaan
from .serializers import DataObatSerializer, BukuPenerimaanSerializer

class DataObatViewSet(viewsets.ModelViewSet):
    search_fields = ['nama_obat']
    filter_backends = (filters.SearchFilter,)
    queryset = DataObat.objects.all().order_by('nama_obat')
    serializer_class = DataObatSerializer
    permission_classes = [permissions.IsAuthenticated]

class PenerimaanViewSet(viewsets.ModelViewSet):
    queryset = BukuPenerimaan.objects.all()
    serializer_class = BukuPenerimaanSerializer
    permission_classes = [permissions.IsAuthenticated]