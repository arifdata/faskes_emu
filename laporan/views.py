from django.shortcuts import render
from django.http import HttpResponse
from poli.models import DataKunjungan
from apotek.models import Resep
import datetime
from collections import OrderedDict
import operator

# Create your views here.
def index_page(request):

    # get tanggal sekarang
    now = datetime.datetime.now()

    #dict utk menampung data sementara
    raw_data_kunjungan = {}
    raw_data_penyakit = {}
    raw_data_obat = {}

    #query data dari awal bulan sekarang sampai sekarang
    query = DataKunjungan.objects.filter(tgl_kunjungan__gte="{}-{}-1".format(now.year, now.month), tgl_kunjungan__lte="{}-{}-{}".format(now.year, now.month, now.day))

    # memasukkan diagnosa ke raw_data_penyakit dan menghitung akumulasinya
    for data in query:
        for diag in data.diagnosa.values('diagnosa'):
            if diag['diagnosa'] not in raw_data_penyakit:
                raw_data_penyakit[diag['diagnosa']] = 1
            else:
                raw_data_penyakit[diag['diagnosa']] += 1
    
    # memasukkan tanggal beserta jumlah kunjungannya respectively ke dict raw_data_kunjungan
    for data in query:
        #print(data.diagnosa.values('diagnosa'))
        b = DataKunjungan.objects.filter(tgl_kunjungan=data.tgl_kunjungan)
        raw_data_kunjungan[data.tgl_kunjungan.strftime('%d-%m')] = len(b)

    # mengurutkan data sesuai urutan tanggal
    cleaned_data_kunjungan = OrderedDict(sorted(raw_data_kunjungan.items()))

    # mengurutkan data sesuai urutan tanggal
    cleaned_data_penyakit = OrderedDict(sorted(raw_data_penyakit.items()))

    query_obat = Resep.objects.filter(kunjungan_pasien__tgl_kunjungan__gte="{}-{}-1".format(now.year, now.month), kunjungan_pasien__tgl_kunjungan__lte="{}-{}-{}".format(now.year, now.month, now.day))

    # Handling perhitungan jumlah obat terpakai
    for data in query_obat:
        #print(data.nama_obat.nama_obat.nama_obat)
        if data.nama_obat.nama_obat.nama_obat not in raw_data_obat:
            raw_data_obat[data.nama_obat.nama_obat.nama_obat] = data.jumlah
        else:
            raw_data_obat[data.nama_obat.nama_obat.nama_obat] += data.jumlah

    # urutkan dictionary obat berdasarkan jumlah terbanyak
    cleaned_data_obat = dict(sorted(raw_data_obat.items(), key=operator.itemgetter(1),reverse=True))

    context = {

        'nama': 'Power User', 
        'bln': now.strftime("%B"), 
        'thn': now.year, 
        'labels_penyakit': list(cleaned_data_penyakit.keys()), 
        'data_penyakit': list(cleaned_data_penyakit.values()), 
        'labels_kunjungan': list(cleaned_data_kunjungan.keys()), 
        'data_kunjungan': list(cleaned_data_kunjungan.values()),
        'labels_obat_terbanyak': list(cleaned_data_obat.keys())[0:10],
        'data_obat_terbanyak': list(cleaned_data_obat.values())[0:10]

    }

    return render(request, 'laporan/index.html', context)

def laporan_page(request):
    return render(request, 'laporan/laporan_generator.html')