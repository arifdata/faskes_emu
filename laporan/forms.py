from django import forms
import datetime

class NameForm(forms.Form):
    tanggal1 = forms.CharField(label="Tanggal Awal", widget=forms.widgets.DateTimeInput(attrs={"type": "date"}))
    tanggal2 = forms.CharField(label="Tanggal Akhir", widget=forms.widgets.DateTimeInput(attrs={"type": "date"}))
