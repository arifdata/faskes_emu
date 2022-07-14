from rest_framework import serializers
from .models import Diagnosa

class DiagnosaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosa
        fields = ['diagnosa']