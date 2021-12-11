from django import forms
import datetime

class TglForm(forms.Form):
    tanggal1 = forms.CharField(label="Tanggal Awal", widget=forms.widgets.DateTimeInput(attrs={"type": "date"}))
    tanggal2 = forms.CharField(label="Tanggal Akhir", widget=forms.widgets.DateTimeInput(attrs={"type": "date"}))

class TglChoiceForm(forms.Form):
    CHOICES = [('apotek', 'Apotek'), ('gudang', 'Gudang')]
    tanggal1 = forms.CharField(label="Tanggal Awal", widget=forms.widgets.DateTimeInput(attrs={"type": "date"}))
    tanggal2 = forms.CharField(label="Tanggal Akhir", widget=forms.widgets.DateTimeInput(attrs={"type": "date"}))
    pilihan = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
