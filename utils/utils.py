from django.http import FileResponse
from pendaftaran.models import DataPasien
from apotek.models import DataObat
from django.contrib.auth.decorators import login_required
import csv
import datetime

@login_required
def download_backup(request):
    timestamp = datetime.datetime.now()
    return FileResponse(open('db.sqlite3', 'rb'), as_attachment=True, filename="backup_faskes-emu_{}.sqlite3".format(timestamp.strftime("%Y-%b-%d")))
    

def init_data_pasien():
    with open('utils/master_pasien.csv', 'r') as f:
        rd = csv.reader(f)
        for i in rd:
            a = DataPasien(no_kartu=i[1], nama_pasien=i[0], alamat=i[3], usia=datetime.datetime.strptime(i[2], '%d-%m-%Y'), no_hp=0000)
            a.save()
            print("Menginput {} {} {} {}".format(i[0], i[1], i[2], i[3]))

def init_data_obat():
    with open('utils/master_obat.csv', 'r') as f:
        rd = csv.reader(f)
        for i in rd:
            a = DataObat(nama_obat=i[0], satuan=i[1], is_ab=i[2], is_okt=i[3], is_non_generik=i[4], is_alkes=i[5], is_jkn=i[6])
            a.save()
            print(i[0], i[1], i[2])
