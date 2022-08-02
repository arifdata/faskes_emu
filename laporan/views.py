from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from collections import OrderedDict, Counter
import operator
from socket import gethostname, gethostbyname

# Create your views here.
def contact_developer(request):
    return render(request, 'laporan/hubungi_developer.html')
    
def index_page(request):
    import datetime
    from statistics import mean
    from poli.models import DataKunjungan
    from apotek.models import Resep, Pengeluaran, Penerimaan
    # get tanggal sekarang
    now = datetime.datetime.now()
    three_month_before = now - datetime.timedelta(days=90)
    three_month_after = now + datetime.timedelta(days=90)

    #dict utk menampung data sementara
    raw_data_kunjungan = {}
    raw_data_penyakit = {}
    raw_data_obat = {}
    raw_data_penulis = {}
    raw_data_ed = {}

    ed = Penerimaan.objects.select_related('nama_barang').filter(tgl_kadaluarsa__gte=f"{three_month_before.year}-{three_month_before.month}-{three_month_before.day}", tgl_kadaluarsa__lte=f"{three_month_after.year}-{three_month_after.month}-{three_month_after.day}").iterator()

    for i in ed:
        raw_data_ed[i.nama_barang.nama_obat] = [f"{i.tgl_kadaluarsa.year}-{i.tgl_kadaluarsa.month}-{i.tgl_kadaluarsa.day}", f"{(i.tgl_kadaluarsa + datetime.timedelta(days=2)).year}-{(i.tgl_kadaluarsa + datetime.timedelta(days=2)).month}-{(i.tgl_kadaluarsa + datetime.timedelta(days=2)).day}"]

    #query data dari awal bulan sekarang sampai sekarang
    query = DataKunjungan.objects.select_related('penulis_resep').filter(tgl_kunjungan__gte="{}-{}-1".format(now.year, now.month), tgl_kunjungan__lte="{}-{}-{}".format(now.year, now.month, now.day))

    # hitung penulis resep
    for data in query:
        if data.penulis_resep.nama_peresep not in raw_data_penulis:
            raw_data_penulis[data.penulis_resep.nama_peresep] = 1
        else:
            raw_data_penulis[data.penulis_resep.nama_peresep] += 1

    # memasukkan diagnosa ke raw_data_penyakit dan menghitung akumulasinya
    for data in query:
        for diag in data.diagnosa.values('diagnosa'):
            if diag['diagnosa'] not in raw_data_penyakit:
                raw_data_penyakit[diag['diagnosa']] = 1
            else:
                raw_data_penyakit[diag['diagnosa']] += 1
    
    # memasukkan tanggal beserta jumlah kunjungannya respectively ke dict raw_data_kunjungan
    for data in query:
        b = DataKunjungan.objects.filter(tgl_kunjungan=data.tgl_kunjungan).count()
        raw_data_kunjungan[data.tgl_kunjungan.strftime('%d-%m')] = b

    # mengurutkan data sesuai urutan tanggal
    cleaned_data_kunjungan = OrderedDict(sorted(raw_data_kunjungan.items()))

    # mengurutkan data sesuai urutan tanggal
    cleaned_data_penyakit = OrderedDict(sorted(raw_data_penyakit.items()))

    query_obat = Resep.objects.select_related('nama_obat__nama_obat').filter(kunjungan_pasien__tgl_kunjungan__gte="{}-{}-1".format(now.year, now.month), kunjungan_pasien__tgl_kunjungan__lte="{}-{}-{}".format(now.year, now.month, now.day)).iterator()

    # Handling perhitungan jumlah obat terpakai
    for data in query_obat:
        if data.nama_obat.nama_obat.nama_obat not in raw_data_obat:
            raw_data_obat[data.nama_obat.nama_obat.nama_obat] = data.jumlah
        else:
            raw_data_obat[data.nama_obat.nama_obat.nama_obat] += data.jumlah

    # urutkan dictionary obat berdasarkan jumlah terbanyak
    cleaned_data_obat = dict(sorted(raw_data_obat.items(), key=operator.itemgetter(1),reverse=True))
    
    rerata = 0
    if len(list(cleaned_data_kunjungan.values())) > 0:
        rerata = mean(list(cleaned_data_kunjungan.values()))

    addr = gethostbyname(gethostname())
    if addr == "127.0.0.1":
        addr = ""
        
    penyakit = [{'x':k, 'y':v} for k, v in cleaned_data_penyakit.items()]
    maksimum = 0 if len(cleaned_data_kunjungan.values()) == 0 else max(list(cleaned_data_kunjungan.values()))

    context = {
        'bln': now.strftime("%B"), 
        'thn': now.year, 
        'labels_kunjungan': list(cleaned_data_kunjungan.keys()), 
        'data_kunjungan': list(cleaned_data_kunjungan.values()),
        'rerata_kunjungan': rerata,
        'maks': maksimum,
        'labels_obat_terbanyak': list(cleaned_data_obat.keys())[0:20],
        'data_obat_terbanyak': list(cleaned_data_obat.values())[0:20],
        'addr': addr,
        'labels_penulis_resep': list(raw_data_penulis.keys()),
        'data_penulis_resep': list(raw_data_penulis.values()),
        'penyakit': penyakit,
        'ed': raw_data_ed,
    }

    return render(request, 'laporan/index.html', context)

def laporan_page(request):
    return render(request, 'laporan/laporan_generator.html')

@login_required
def so_apotek(request):
    if request.method == 'POST':
        pass
    else:
        pass

@login_required
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
            
            q = Resep.objects.select_related('nama_obat__nama_obat').filter(kunjungan_pasien__tgl_kunjungan__gte=request.POST.get("tanggal1"), kunjungan_pasien__tgl_kunjungan__lte=request.POST.get("tanggal2")).iterator()
            q2 = Pengeluaran.objects.select_related('nama_barang__nama_obat').filter(keluar_barang__tgl_keluar__gte=request.POST.get("tanggal1"), keluar_barang__tgl_keluar__lte=request.POST.get("tanggal2")).exclude(keluar_barang__tujuan__nama="APOTEK").iterator()

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
        q = KartuStokApotek.objects.select_related('nama_obat').filter(tgl__gte=tgl_awal, tgl__lte=tgl_akhir)
    else:
        q = KartuStokGudang.objects.select_related('nama_obat').filter(tgl__gte=tgl_awal, tgl__lte=tgl_akhir)
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

@login_required
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
            ft = Font(name='Calibri', size=6.5)
            brd = Border(left=Side(border_style='thin', color='000000'),
                        right=Side(border_style='thin', color='000000'),
                        top=Side(border_style='thin', color='000000'),
                        bottom=Side(border_style='thin', color='000000'))
            
            wb = Workbook()
            del wb["Sheet"]
            try:
                for obat, data in raw_data.items():
                    no_char = "/\[]*?:"
                    for c in no_char:
                        if c in obat:
                            obat = obat.replace(c, " ")
                        else:
                            pass
                    ws = wb.create_sheet(obat)
                    ws.set_printer_settings(5, ws.ORIENTATION_LANDSCAPE)
                    ws.page_margins.left = 0.2
                    ws.page_margins.right = 0.2
                    ws.page_margins.bottom = 0.2
                    ws.page_margins.top = 0.2

                    for idx, rows in enumerate(data):
                        if idx % 34 == 0:
                            #ws.append(["KARTU STOK{}".format(90 * " ")])
                            ws.append(["KARTU STOK"])
                            ws.append(["Item : {}".format(obat.title())])
                            ws.append(["Lokasi : {}".format(request.POST.get("pilihan").title())])
                            ws.append(["{}".format(110 * " ")])
                            ws.append(["Tanggal", "Unit|Batch", "Terima", "Keluar", "Sisa", "Ket/ED"])
                            ws.append(rows)
                        else:
                            ws.append(rows)

                    for cells in ws.rows:
                        for cell in cells:
                            if cell.value == "KARTU STOK" or str(cell.value).startswith("Item") or str(cell.value).startswith("Lokasi"):
                                cell.border = brd
                                cell.font = Font(name='Calibri', size=7, bold=True)
                                cell.alignment = Alignment(horizontal='center')
                                ws.merge_cells('A{}:F{}'.format(cell.row, cell.row))
                            elif cell.value == "Tanggal" or cell.value == "Unit|Batch" or cell.value == "Terima" or cell.value == "Keluar" or cell.value == "Sisa" or cell.value == "Ket/ED":
                                cell.font = Font(name='Calibri', size=7, bold=True)
                                cell.border = brd
                                cell.alignment = Alignment(horizontal='center')
                            else:
                                cell.font = ft
                                cell.border = brd
                            
                    ws.column_dimensions['A'].width = 7
                    ws.column_dimensions['B'].width = 9
                    ws.column_dimensions['C'].width = 4
                    ws.column_dimensions['D'].width = 4
                    ws.column_dimensions['E'].width = 4
                    ws.column_dimensions['F'].width = 6

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

@login_required
def lap_narko_psiko(request):
    from .forms import TglForm
    import json
    if request.method == 'POST':
        form = TglForm(request.POST)
        if form.is_valid():
            raw_data = {}
            kunci = []
            from apotek.models import Resep
            q = Resep.objects.select_related('kunjungan_pasien', 'nama_obat__nama_obat').filter(kunjungan_pasien__tgl_kunjungan__gte=request.POST.get("tanggal1"), kunjungan_pasien__tgl_kunjungan__lte=request.POST.get("tanggal2")).filter(nama_obat__nama_obat__is_okt=True)
            
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

def tengok_stok_alkes(request):
    from apotek.models import StokObatGudang
    q = StokObatGudang.objects.select_related('nama_obat').filter(nama_obat__is_alkes=True)
    alkes = {}
    for item in q:
        if item.jml > 0:
            alkes[item.nama_obat.nama_obat] = [item.nama_obat.satuan, "ada"]
        else:
            alkes[item.nama_obat.nama_obat] = [item.nama_obat.satuan, "kosong"]

    alkes = OrderedDict(sorted(alkes.items()))
    ctx = {
        'data': alkes,
    }
    return render(request, 'laporan/tengok_stok_alkes.html', context=ctx)

def tengok_stok_obat(request):
    from apotek.models import StokObatGudang, StokObatApotek

    okt = {}
    q = StokObatGudang.objects.select_related('nama_obat').filter(nama_obat__is_okt=True)
    for item in q:
        okt[item.nama_obat.nama_obat] = [item.nama_obat.satuan, item.jml]
    q = StokObatApotek.objects.select_related('nama_obat').filter(nama_obat__is_okt=True)
    for item in q:
        if item.nama_obat.nama_obat not in okt:
            okt[item.nama_obat.nama_obat] = [item.nama_obat.satuan, item.jml]
        else:
            okt[item.nama_obat.nama_obat][1] += item.jml
    okt = OrderedDict(sorted(okt.items()))

    ab = {}
    q = StokObatGudang.objects.select_related('nama_obat').filter(nama_obat__is_ab=True)
    for item in q:
        ab[item.nama_obat.nama_obat] = [item.nama_obat.satuan, item.jml]
    q = StokObatApotek.objects.select_related('nama_obat').filter(nama_obat__is_ab=True)
    for item in q:
        if item.nama_obat.nama_obat not in ab:
            ab[item.nama_obat.nama_obat] = [item.nama_obat.satuan, item.jml]
        else:
            ab[item.nama_obat.nama_obat][1] += item.jml
    ab = OrderedDict(sorted(ab.items()))

    obt = {}
    q = StokObatGudang.objects.select_related('nama_obat').filter(nama_obat__is_alkes=False, nama_obat__is_ab=False, nama_obat__is_okt=False)
    for item in q:
        obt[item.nama_obat.nama_obat] = [item.nama_obat.satuan, item.jml]
    q = StokObatApotek.objects.select_related('nama_obat').filter(nama_obat__is_ab=True)
    for item in q:
        if item.nama_obat.nama_obat not in obt:
            obt[item.nama_obat.nama_obat] = [item.nama_obat.satuan, item.jml]
        else:
            obt[item.nama_obat.nama_obat][1] += item.jml
    obt = OrderedDict(sorted(obt.items()))
            
    ctx = {
        'okt': okt,
        'antibiotik': ab,
        'obat': obt,
    }
    return render(request, 'laporan/tengok_stok_obat.html', context=ctx)

@login_required
def so_apotek(request):
    from .forms import SingleTgl
    from apotek.models import StokObatApotek, KartuStokApotek

    stok_apotek = StokObatApotek.objects.all()
    form = SingleTgl(request.POST)
    context = {
        'data': stok_apotek
    }
    context['form'] = form
    
    if request.method == 'POST':
        if form.is_valid():
            
            #print(form['tanggal'].value())
            
            for obat in stok_apotek:
                #Ubah jumlah stok sesuai value yg diinput

                if int(request.POST[obat.nama_obat.nama_obat]) != obat.jml:
                    obat.jml = request.POST[obat.nama_obat.nama_obat]
                    obat.save()

                #Penyesuaian kartu stok tiap item
                query_kartu_apt = KartuStokApotek.objects.filter(nama_obat__nama_obat=obat)
                stok_apt_sebelum = query_kartu_apt[len(query_kartu_apt)-1]

                #Bila stok fisik lebih kecil daripada stok tercatat sebelumnya
                if int(request.POST[obat.nama_obat.nama_obat]) < stok_apt_sebelum.sisa_stok:
                    selisih = stok_apt_sebelum.sisa_stok - int(request.POST[obat.nama_obat.nama_obat])
                    kartu_stok_apt_input = KartuStokApotek(nama_obat=obat.nama_obat, tgl=form['tanggal'].value(), unit="Staf", stok_keluar=selisih, sisa_stok=int(request.POST[obat.nama_obat.nama_obat]), ref=obat.id)
                    kartu_stok_apt_input.save()
                    
            """
            for obat in stok_apotek:
                print(request.POST[obat.nama_obat.nama_obat])
            """
            return render(request, 'laporan/so_apotek.html', context)
            
    else:
        return render(request, 'laporan/so_apotek.html', context)

@login_required
def lap_generik(request):
    from .forms import GenerikForm
    
    if request.method == 'POST':
        from apotek.models import Resep
        from poli.models import DataKunjungan
        form = GenerikForm(request.POST)
        if form.is_valid():
            try:
                jml_lbr = DataKunjungan.objects.filter(tgl_kunjungan__gte=request.POST.get("tanggal1"), tgl_kunjungan__lte=request.POST.get("tanggal2")).filter(penulis_resep__nama_peresep=request.POST.get("pilihan")).count()

                tot_r = Resep.objects.filter(kunjungan_pasien__tgl_kunjungan__gte=request.POST.get("tanggal1"), kunjungan_pasien__tgl_kunjungan__lte=request.POST.get("tanggal2")).filter(kunjungan_pasien__penulis_resep__nama_peresep=request.POST.get("pilihan")).count()
                
                r_generik = Resep.objects.filter(kunjungan_pasien__tgl_kunjungan__gte=request.POST.get("tanggal1"), kunjungan_pasien__tgl_kunjungan__lte=request.POST.get("tanggal2")).filter(kunjungan_pasien__penulis_resep__nama_peresep=request.POST.get("pilihan")).filter(nama_obat__nama_obat__is_non_generik=True).count()
                
                ctx = {
                    'kalkulasi': {
                        'peresep': request.POST.get("pilihan"),
                        'jml_lembar': jml_lbr,
                        'total_resep': tot_r,
                        'resep_generik': tot_r - r_generik,
                        'persentase': "{0:.2f} %".format((tot_r - r_generik) / tot_r * 100),
                    },
                }
                ctx['form'] = form

                return render(request, 'laporan/form_lap_generik.html', context=ctx)

            except:
                return HttpResponse("Tidak ada data. Coba tanggal atau pilihan lain.")
    else:
        form = GenerikForm()
        
    return render(request, 'laporan/form_lap_generik.html', {'form': form})

@login_required
def lap_por(request):
    from .forms import PorForm
    if request.method == 'POST':
        from apotek.models import Resep
        form = PorForm(request.POST)
        if form.is_valid():
            try:
                #refdose = dict(Resep.ATURAN_PK)
                counter = 1
                raw_data = {}
                q = Resep.objects.select_related('kunjungan_pasien__nama_pasien', 'nama_obat__nama_obat').filter(kunjungan_pasien__tgl_kunjungan__gte=request.POST.get("tanggal1"), kunjungan_pasien__tgl_kunjungan__lte=request.POST.get("tanggal2")).filter(kunjungan_pasien__diagnosa__diagnosa=request.POST.get("pilihan")).order_by('kunjungan_pasien__tgl_kunjungan').iterator()
                
                for data in q:
                    if not raw_data:
                        raw_data[counter] = {"nama": data.kunjungan_pasien.nama_pasien.nama_pasien, "tgl": data.kunjungan_pasien.tgl_kunjungan.strftime("%Y-%m-%d"), "obat": [(data.nama_obat.nama_obat.nama_obat, data.aturan_pakai, data.lama_pengobatan, data.jumlah, data.nama_obat.nama_obat.is_ab)], "id": data.kunjungan_pasien.id, "usia": data.kunjungan_pasien.nama_pasien.umur()}
                    elif data.kunjungan_pasien.nama_pasien.nama_pasien == raw_data[counter]["nama"] and data.kunjungan_pasien.id == raw_data[counter]["id"]:
                        raw_data[counter]["obat"].append((data.nama_obat.nama_obat.nama_obat, data.aturan_pakai, data.lama_pengobatan, data.jumlah, data.nama_obat.nama_obat.is_ab))
                    else:
                        counter += 1
                        raw_data[counter] = {"nama": data.kunjungan_pasien.nama_pasien.nama_pasien, "tgl": data.kunjungan_pasien.tgl_kunjungan.strftime("%Y-%m-%d"), "obat": [(data.nama_obat.nama_obat.nama_obat, data.aturan_pakai, data.lama_pengobatan, data.jumlah, data.nama_obat.nama_obat.is_ab)], "id": data.kunjungan_pasien.id, "usia": data.kunjungan_pasien.nama_pasien.umur()}
                        
                ctx = {
                    'data': raw_data,
                    'input': {
                        'date1': request.POST.get("tanggal1"),
                        'date2': request.POST.get("tanggal2"),
                        'diag': request.POST.get("pilihan"),
                    }
                }
                return render(request, 'laporan/lap_por.html', context=ctx)

            except Exception as e:
                return HttpResponse(e)

    else:
        form = PorForm()
    return render(request, 'laporan/form_lap_por.html', {'form': form})
    