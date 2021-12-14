from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from collections import OrderedDict, Counter
import operator

# Create your views here.
def index_page(request):
    import datetime
    from statistics import mean
    from poli.models import DataKunjungan
    from apotek.models import Resep, Pengeluaran
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
    #print()

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
        'bln': now.strftime("%B"), 
        'thn': now.year, 
        'labels_penyakit': list(cleaned_data_penyakit.keys()), 
        'data_penyakit': list(cleaned_data_penyakit.values()), 
        'labels_kunjungan': list(cleaned_data_kunjungan.keys()), 
        'data_kunjungan': list(cleaned_data_kunjungan.values()),
        'rerata_kunjungan': mean(list(cleaned_data_kunjungan.values())),
        'labels_obat_terbanyak': list(cleaned_data_obat.keys())[0:10],
        'data_obat_terbanyak': list(cleaned_data_obat.values())[0:10]
    }

    return render(request, 'laporan/index.html', context)

def laporan_page(request):
    return render(request, 'laporan/laporan_generator.html')

def penggunaan_bmhp(request):
    from apotek.models import Resep, Pengeluaran
    from .forms import TglForm
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TglForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            raw_data_bmhp_apt = {}
            raw_data_bmhp_unit = {}
            kunci = []
            cleaned_data_bmhp_unit = {}
            """
            for key, value in request.POST.items():
                print('Key: %s' % (key) ) 
                print('Value %s' % (value) )
            """
            q = Resep.objects.filter(kunjungan_pasien__tgl_kunjungan__gte=request.POST.get("tanggal1"), kunjungan_pasien__tgl_kunjungan__lte=request.POST.get("tanggal2"))
            q2 = Pengeluaran.objects.filter(keluar_barang__tgl_keluar__gte=request.POST.get("tanggal1"), keluar_barang__tgl_keluar__lte=request.POST.get("tanggal2")).exclude(keluar_barang__tujuan__nama="APOTEK")

            for data in q:
                if data.nama_obat.nama_obat.nama_obat not in raw_data_bmhp_apt:
                    raw_data_bmhp_apt[data.nama_obat.nama_obat.nama_obat] = data.jumlah
                else:
                    raw_data_bmhp_apt[data.nama_obat.nama_obat.nama_obat] += data.jumlah

            cleaned_data_obat = dict(sorted(raw_data_bmhp_apt.items(), key=operator.itemgetter(1),reverse=True))
            cleaned_data_obat = OrderedDict(sorted(cleaned_data_obat.items()))

            for data in q2:
                a = {}
                a[data.nama_barang.nama_obat.nama_obat] = data.jumlah
                if data.keluar_barang.tujuan.nama not in raw_data_bmhp_unit.keys():
                    raw_data_bmhp_unit[data.keluar_barang.tujuan.nama] = [a]
                    kunci.append(data.keluar_barang.tujuan.nama)
                else:                    
                    raw_data_bmhp_unit[data.keluar_barang.tujuan.nama].append(a)

            for d in kunci:
                c = Counter()
                for x in raw_data_bmhp_unit[d]:
                    c.update(x)
                    cleaned_data_bmhp_unit[d] = dict(c)
            
            context = {
                'startdate': request.POST.get("tanggal1"),
                'enddate': request.POST.get("tanggal2"),
                'val': cleaned_data_obat,
                'unit': cleaned_data_bmhp_unit,
            }
            return render(request, 'laporan/penggunaan_bmhp.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TglForm()

    return render(request, 'laporan/form_penggunaan_bmhp.html', {'form': form})

def pilih_kartu(kartu, tgl_awal, tgl_akhir):
    from apotek.models import KartuStokApotek, KartuStokGudang
    if kartu == "apotek":
        q = KartuStokApotek.objects.filter(tgl__gte=tgl_awal, tgl__lte=tgl_akhir)
    else:
        q = KartuStokGudang.objects.filter(tgl__gte=tgl_awal, tgl__lte=tgl_akhir)
    item_set, raw_data = [], {}
    
    for x in q:
        item_set.append(x.nama_obat.nama_obat)
    item_set = list(set(item_set))

    for item in item_set:
        raw_data[item] = []
        data = q.filter(nama_obat__nama_obat=item)
        for x in data:
            raw_data[item].append([x.tgl.strftime("%Y-%m-%d"), x.unit.title(), x.stok_terima, x.stok_keluar, x.sisa_stok, x.ket])

    #pprint.pprint(raw_data)
    return raw_data

def cetak_kartu_stok(request):
    from .forms import TglChoiceForm
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TglChoiceForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            from openpyxl.workbook import Workbook
            from openpyxl.styles import Border, Font, Side, Alignment
            from tempfile import NamedTemporaryFile
            
            raw_data = pilih_kartu(request.POST.get("pilihan"), request.POST.get("tanggal1"), request.POST.get("tanggal2"))
            ft = Font(name='Calibri', size=8)
            brd = Border(left=Side(border_style='thin', color='000000'),
                        right=Side(border_style='thin', color='000000'),
                        top=Side(border_style='thin', color='000000'),
                        bottom=Side(border_style='thin', color='000000'))
            
            wb = Workbook()
            del wb["Sheet"]
            try:
                for obat, data in raw_data.items():
                    ws = wb.create_sheet(obat)
                    ws.set_printer_settings(5, ws.ORIENTATION_LANDSCAPE)
                    ws.page_margins.left = 0.2
                    ws.page_margins.right = 0.2
                    ws.page_margins.bottom = 0.2
                    ws.page_margins.top = 0.2

                    for idx, rows in enumerate(data):
                        if idx % 36 == 0:
                            #ws.append(["KARTU STOK{}".format(90 * " ")])
                            ws.append(["KARTU STOK"])
                            ws.append(["Item : {}".format(obat.title())])
                            ws.append(["Lokasi : {}".format(request.POST.get("pilihan").title())])
                            ws.append(["{}".format(110 * " ")])
                            ws.append(["Tanggal", "Unit", "Terima", "Keluar", "Sisa", "Ket"])
                            ws.append(rows)
                        else:
                            ws.append(rows)

                    for cells in ws.rows:
                        for cell in cells:
                            if cell.value == "KARTU STOK" or str(cell.value).startswith("Item") or str(cell.value).startswith("Lokasi"):
                                cell.border = brd
                                cell.font = Font(name='Calibri', size=8, bold=True)
                                cell.alignment = Alignment(horizontal='center')
                                ws.merge_cells('A{}:F{}'.format(cell.row, cell.row))
                            elif cell.value == "Tanggal" or cell.value == "Unit" or cell.value == "Terima" or cell.value == "Keluar" or cell.value == "Sisa" or cell.value == "Ket":
                                cell.font = Font(name='Calibri', size=8, bold=True)
                                cell.border = brd
                                cell.alignment = Alignment(horizontal='center')
                            else:
                                cell.font = ft
                                cell.border = brd
                            
                    ws.column_dimensions['A'].width = 8
                    ws.column_dimensions['B'].width = 6
                    ws.column_dimensions['C'].width = 5
                    ws.column_dimensions['D'].width = 5
                    ws.column_dimensions['E'].width = 5
                    ws.column_dimensions['F'].width = 5

                tmp = NamedTemporaryFile(delete=False)
                with open(tmp.name) as fi:
                    wb.save(tmp.name)
                    return FileResponse(open(tmp.name, 'rb'), as_attachment=True, filename="kartu_stok_{}_{}_to_{}.xlsx".format(request.POST.get("pilihan"), request.POST.get("tanggal1"), request.POST.get("tanggal2")))

            except IndexError:
                ctx = {
                    'gagal': "Tidak ada data. Coba tanggal lain!",
                }
                ctx.update({'form': form})
                #return return render(request, 'laporan/form_cetak_kartu.html', {'form': form})
                return render(request, 'laporan/form_cetak_kartu.html', context=ctx)


    # if a GET (or any other method) we'll create a blank form
    else:
        form = TglChoiceForm()

    return render(request, 'laporan/form_cetak_kartu.html', {'form': form})

def lap_narko_psiko(request):
    from .forms import TglForm
    import json
    if request.method == 'POST':
        form = TglForm(request.POST)
        if form.is_valid():
            raw_data = {}
            kunci = []
            from apotek.models import Resep
            q = Resep.objects.filter(kunjungan_pasien__tgl_kunjungan__gte=request.POST.get("tanggal1"), kunjungan_pasien__tgl_kunjungan__lte=request.POST.get("tanggal2")).filter(nama_obat__nama_obat__is_okt=True)
            
            for object in q:
                kunci.append(object.nama_obat.nama_obat.nama_obat)
            kunci = list(set(kunci))
            kunci.sort()

            for item in kunci:
                r = q.filter(nama_obat__nama_obat__nama_obat=item)
                for data in r:                    
                    if item not in raw_data.keys():
                        raw_data[item] = [[
                            data.kunjungan_pasien.tgl_kunjungan.strftime('%Y-%m-%d'),
                            data.kunjungan_pasien.nama_pasien.nama_pasien,
                            "{} tahun".format(data.kunjungan_pasien.nama_pasien.umur()),
                            data.kunjungan_pasien.nama_pasien.alamat,
                            data.kunjungan_pasien.penulis_resep.nama_peresep,
                            data.jumlah,
                            data.nama_obat.nama_obat.satuan,
                        ]]
                    else:
                        raw_data[item].append([
                            data.kunjungan_pasien.tgl_kunjungan.strftime('%Y-%m-%d'),
                            data.kunjungan_pasien.nama_pasien.nama_pasien,
                            "{} tahun".format(data.kunjungan_pasien.nama_pasien.umur()),
                            data.kunjungan_pasien.nama_pasien.alamat,
                            data.kunjungan_pasien.penulis_resep.nama_peresep,
                            data.jumlah,
                            data.nama_obat.nama_obat.satuan,
                        ])
                        
        ctx = {
            'data': raw_data,
            'startdate': request.POST.get("tanggal1"),
            'enddate': request.POST.get("tanggal2"),
        }
        #return HttpResponse(json.dumps(raw_data), content_type="application/json")
        return render(request, 'laporan/lap_narko_psiko.html', context=ctx)
    else:
        form = TglForm()
        return render(request, 'laporan/form_lap_narko_psiko.html', {'form': form})
