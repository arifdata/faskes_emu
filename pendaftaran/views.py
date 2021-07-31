from django.shortcuts import render
from django.http import HttpResponse
from poli.models import DataKunjungan
import datetime
from collections import OrderedDict

# Create your views here.
def index_page(request):

    # get tanggal sekarang
    now = datetime.datetime.now()
    raw_data_penyakit = {}

    #query data dari awal bulan sekarang sampai sekarang
    query = DataKunjungan.objects.filter(tgl_kunjungan__gte="{}-{}-1".format(now.year, now.month), tgl_kunjungan__lte="{}-{}-{}".format(now.year, now.month, now.day))

    # memasukkan diagnosa ke raw_data_penyakit dan menghitung akumulasinya
    for data in query:
        for diag in data.diagnosa.values('diagnosa'):
            if diag['diagnosa'] not in raw_data_penyakit:
                raw_data_penyakit[diag['diagnosa']] = 1
            else:
                raw_data_penyakit[diag['diagnosa']] += 1

    #dict utk menampung data sementara
    raw_data_kunjungan = {}
    
    # memasukkan tanggal beserta jumlah kunjungannya respectively ke dict raw_data_kunjungan
    for data in query:
        #print(data.diagnosa.values('diagnosa'))
        b = DataKunjungan.objects.filter(tgl_kunjungan=data.tgl_kunjungan)
        raw_data_kunjungan[data.tgl_kunjungan.strftime('%d-%m')] = len(b)

    # mengurutkan data sesuai urutan tanggal
    cleaned_data_kunjungan = OrderedDict(sorted(raw_data_kunjungan.items()))

    # mengurutkan data sesuai urutan tanggal
    cleaned_data_penyakit = OrderedDict(sorted(raw_data_penyakit.items()))
    
    print(cleaned_data_penyakit)

    context = {'nama': 'Power User', 'labels_penyakit': list(cleaned_data_penyakit.keys()), 'data_penyakit': list(cleaned_data_penyakit.values()), 'labels_kunjungan': list(cleaned_data_kunjungan.keys()), 'data_kunjungan': list(cleaned_data_kunjungan.values())}
    return render(request, 'pendaftaran/index.html', context)