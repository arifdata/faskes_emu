from django.shortcuts import render
from django.http import HttpResponse
from poli.models import DataKunjungan
import datetime
from collections import OrderedDict

# Create your views here.
def index_page(request):

    # get tanggal sekarang
    now = datetime.datetime.now()

    #query data dari awal bulan sekarang sampai sekarang
    query = DataKunjungan.objects.filter(tgl_kunjungan__gte="{}-{}-1".format(now.year, now.month), tgl_kunjungan__lte="{}-{}-{}".format(now.year, now.month, now.day))

    #dict utk menampung data sementara
    raw_data = {}

    # memasukkan tanggal beserta jumlah kunjungannya respectively ke dict raw_data
    for data in query:
        b = DataKunjungan.objects.filter(tgl_kunjungan=data.tgl_kunjungan)
        raw_data[data.tgl_kunjungan.strftime('%d-%m')] = len(b)

    # mengurutkan data sesuai urutan tanggal
    cleaned_data = OrderedDict(sorted(raw_data.items()))

    print(cleaned_data)
    context = {'nama': 'Power User', 'labels': list(cleaned_data.keys()), 'data': list(cleaned_data.values())}
    return render(request, 'pendaftaran/index.html', context)