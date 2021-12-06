from django import forms
import datetime

class NameForm(forms.Form):
    tanggal1 = forms.CharField(label="Tanggal 1", widget=forms.widgets.DateTimeInput(attrs={"type": "date"}))
    tanggal2 = forms.CharField(label="Tanggal 2", widget=forms.widgets.DateTimeInput(attrs={"type": "date"}))
