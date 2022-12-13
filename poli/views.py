from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from .models import Diagnosa
from .serializers import DiagnosaSerializer

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
