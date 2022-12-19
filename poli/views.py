from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import Diagnosa, DataPeresep
from .serializers import DiagnosaSerializer, DataPeresepSerializer

# Create your views here.
class DiagnosaViewSet(viewsets.ModelViewSet):
    search_fields = ['diagnosa']
    filter_backends = (filters.SearchFilter,)
    queryset = Diagnosa.objects.all()
    serializer_class = DiagnosaSerializer
    permission_classes = []
    authentication_classes = []
    pagination_class = None

    def post(self, request):
        serializer = DiagnosaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

class DataPeresepViewSet(viewsets.ModelViewSet):
    search_fields = ['nama_peresep']
    filter_backends = (filters.SearchFilter,)
    queryset = DataPeresep.objects.all()
    serializer_class = DataPeresepSerializer
    permission_classes = []
    authentication_classes = []
    pagination_class = None

    def post(self, request):
        serializer = DataPeresepSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
