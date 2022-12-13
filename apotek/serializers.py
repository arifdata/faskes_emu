from rest_framework import serializers
from .models import DataObat, BukuPenerimaan, Penerimaan, SumberTerima
from drf_writable_nested.serializers import WritableNestedModelSerializer

class DataObatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataObat
        fields = ['id', 'nama_obat', 'satuan', 'is_ab', 'is_okt', 'is_non_generik', 'is_alkes', 'is_jkn']

class DataObat(serializers.ModelSerializer):
    class Meta:
        model = DataObat
        fields = ['nama_obat']

class SumberTerimaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SumberTerima
        fields = ['nama']
        
class PenerimaanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Penerimaan
        fields = ['nama_barang', 'jumlah', 'tgl_kadaluarsa', 'no_batch']

class BukuPenerimaanSerializer(WritableNestedModelSerializer):
    penerimaan_set = PenerimaanSerializer(many=True)
    class Meta:
        model = BukuPenerimaan
        fields = ['tgl_terima', 'sumber', 'notes', 'file_up', 'penerimaan_set']
