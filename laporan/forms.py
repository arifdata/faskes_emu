from django import forms
import datetime

class TglForm(forms.Form):
    tanggal1 = forms.CharField(label="Tanggal Awal", widget=forms.widgets.DateTimeInput(attrs={"type": "date"}))
    tanggal2 = forms.CharField(label="Tanggal Akhir", widget=forms.widgets.DateTimeInput(attrs={"type": "date"}))

class SingleTgl(forms.Form):
    tanggal = forms.CharField(label="Tanggal", widget=forms.widgets.DateTimeInput(attrs={"type": "date"}))

class TglChoiceForm(TglForm):
    CHOICES = [('apotek', 'Apotek'), ('gudang', 'Gudang')]
    pilihan = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

class GenerikForm(TglForm):
    from poli.models import DataPeresep
    CHOICES = sorted([(p.nama_peresep, p.nama_peresep) for p in DataPeresep.objects.all()])
    pilihan = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

class PorForm(TglForm):
    from poli.models import Diagnosa
    CHOICES = sorted([(d.diagnosa, d.diagnosa) for d in Diagnosa.objects.all()])
    pilihan = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

class SOGudangForm(forms.Form):
    from apotek.models import SOGudang
    CHOICES = sorted([tgl.id, tgl.tgl] for tgl in SOGudang.objects.all())
    pilihan = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
