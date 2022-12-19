from rest_framework import serializers
from .models import Diagnosa, DataPeresep

class DiagnosaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosa
        fields = ['id', 'diagnosa']

class DataPeresepSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPeresep
        fields = ['id', 'nama_peresep']
