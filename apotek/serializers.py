from rest_framework import serializers
from .models import DataObat

class DataObatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataObat
        fields = ['nama_obat', 'satuan', 'is_ab', 'is_okt', 'is_non_generik', 'is_alkes', 'is_jkn']