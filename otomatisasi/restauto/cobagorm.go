package restauto

import (
	"bytes"
	"encoding/json"
	"fmt"
	"github.com/xuri/excelize/v2"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"io/ioutil"
	"net/http"
	"strconv"
	"strings"
)

func HurufConvert(s string) int {
	huruf, err := strconv.Atoi(s)
	if err != nil {
		panic(err)
	}
	return huruf
}

func TanggalFixer(s string) *string {
	tgl := strings.Split(s, "-")
	bener := fmt.Sprintf("%s-%s-%s", tgl[2], tgl[1], tgl[0])
	return &bener
}

func CobaGorm() {
	// konek ke sqlite database pake gorm
	db, err := gorm.Open(sqlite.Open("../db.sqlite3"), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}

	// buka file excel penerimaan_epus.xlsx pake excelize
	f, err := excelize.OpenFile("penerimaan_epus.xlsx")
	if err != nil {
		fmt.Println(err)
		return
	}
	defer func() {
		// tutup file excel di akhir scope.
		if err := f.Close(); err != nil {
			fmt.Println(err)
		}
	}()

	// ambil semua baris di Sheet1.
	rows, err := f.GetRows("Sheet1")
	if err != nil {
		fmt.Println(err)
		return
	}

	record_count := 0
	tglterima := ""
	sumberterima := ""

	for index, row := range rows {
		if index == 0 {
			tglterima = row[1]
			sumberterima = row[3]
		} else if index > 3 {
			record_count += 1
			var obat ApotekDataobat
			result := db.First(&obat, "nama_obat = ?", row[1])
			//fmt.Println(obat.NamaObat)

			// handle bila obat belum ada di dalam database
			if result.Error != nil {
				fmt.Printf("\nBarang %s belum masuk dalam database! Masukkan data barangnya:\n", row[1])

				var satuan string
				var ab string
				var okt string
				var nongen string
				var alkes string
				var jkn string

				// ambil input dari user utk data obat baru
				fmt.Println("Masukkan satuan: TAB/SYR/CAP/BKS/TUB/CRM/PCS/BTL/AMP/SET/KTK")
				fmt.Scanln(&satuan)
				fmt.Println("Masukkan angka: 0 = bukan antibiotik. 1 = antibiotik.")
				fmt.Scanln(&ab)
				fmt.Println("Masukkan angka: 0 = bukan OKT. 1 = OKT.")
				fmt.Scanln(&okt)
				fmt.Println("Masukkan angka: 0 = generik. 1 = non generik.")
				fmt.Scanln(&nongen)
				fmt.Println("Masukkan angka: 0 = bukan alkes. 1 = alkes.")
				fmt.Scanln(&alkes)
				fmt.Println("Masukkan angka: 0 = bukan JKN. 1 = JKN.")
				fmt.Scanln(&jkn)

				bmhp_baru := ApotekDataobat{
					NamaObat:     row[1],
					Satuan:       satuan,
					IsAb:         ab,
					IsOkt:        okt,
					IsNonGenerik: nongen,
					IsAlkes:      alkes,
					IsJkn:        jkn,
				}

				//masukkan record baru ke database
				db.Create(&bmhp_baru)
			}
		}
	}

	var sumber ApotekSumberterima
	db.First(&sumber, "nama = ?", sumberterima)
	data := &BukuPenerimaan{}
	data.PenerimaanSet = make([]Penerimaan, record_count)
	data.Sumber = sumber.ID
	data.TanggalTerima = tglterima
	data.Notes = ""
	penerimaan_count := 0

	for index, row := range rows {
		if index > 3 {
			if row[9] != "-" {
				var obat ApotekDataobat
				db.First(&obat, "nama_obat = ?", row[1])
				data.PenerimaanSet[penerimaan_count] = Penerimaan{
					NamaBarang:    obat.ID,
					Jumlah:        HurufConvert(row[4]),
					TglKadaluarsa: TanggalFixer(row[9]),
					NoBatch:       row[8],
				}
				penerimaan_count += 1
			} else {
				var obat ApotekDataobat
				db.First(&obat, "nama_obat = ?", row[1])
				data.PenerimaanSet[penerimaan_count] = Penerimaan{
					NamaBarang:    obat.ID,
					Jumlah:        HurufConvert(row[4]),
					TglKadaluarsa: nil,
					NoBatch:       row[8],
				}
				penerimaan_count += 1
			}
		}

	}

	a, _ := json.Marshal(data)
	req, err := http.NewRequest("POST", "http://localhost:8000/api/bukupenerimaan/", bytes.NewBuffer(a))
	req.SetBasicAuth("admin", "puskesmas")
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	fmt.Println("response Status:", resp.Status)
	body, _ := ioutil.ReadAll(resp.Body)
	fmt.Println("response Body:", string(body))

}
