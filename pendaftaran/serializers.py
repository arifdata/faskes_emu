from rest_framework import serializers
from .models import DataPasien

class DataPasienSerializer(serializers.HyperlinkedModelSerializer):
    usia = serializers.DateField(format='%d-%m-%Y')
    class Meta:
        model = DataPasien
        fields = ['id', 'url', 'no_kartu', 'nama_pasien', 'alamat', 'usia', 'no_hp']