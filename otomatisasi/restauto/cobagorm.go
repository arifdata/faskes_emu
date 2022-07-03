package restauto

import (
	"fmt"
	"github.com/xuri/excelize/v2"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

type ApotekDataobat struct {
	ID           int32  `gorm:"primary_key;AUTO_INCREMENT;column:id;type:integer;"`
	NamaObat     string `gorm:"column:nama_obat;type:varchar;size:200;"`
	Satuan       string `gorm:"column:satuan;type:varchar;size:3;"`
	IsAb         string
	IsOkt        string
	IsNonGenerik string
	IsAlkes      string
	IsJkn        string
}

func (ApotekDataobat) TableName() string {
	return "apotek_dataobat"
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
		// Close the spreadsheet.
		if err := f.Close(); err != nil {
			fmt.Println(err)
		}
	}()

	// Get all the rows in the Sheet1.
	rows, err := f.GetRows("Sheet1")
	if err != nil {
		fmt.Println(err)
		return
	}
	for index, row := range rows {
		// indeks 0 adalah header bukan daftar obat, maka kita abaikan
		if index > 0 {
			var obat ApotekDataobat
			result := db.First(&obat, "nama_obat = ?", row[1])

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

}
