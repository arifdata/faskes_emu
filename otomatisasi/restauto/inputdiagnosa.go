package restauto

import (
	//"encoding/json"
	"fmt"
	"github.com/xuri/excelize/v2"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	//"net/http"
)

func InputDiagnosa() {
	// konek ke sqlite database pake gorm
	db, err := gorm.Open(sqlite.Open("../db.sqlite3"), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}

	// buka file excel pake excelize
	f, err := excelize.OpenFile("Laporan Harian - Pelayanan Pasien.xlsx")
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

	for indeks, row := range rows {
		if indeks > 24 {
			diag_col := []int{54, 56, 58, 60, 62}
			for _, colnum := range diag_col {
				var diag Diagnosa
				result := db.First(&diag, "diagnosa = ?", row[colnum])
				if result.Error != nil {
					newdiag := Diagnosa{Diagnosa: row[colnum]}
					db.Create(&newdiag)
					fmt.Println(row[colnum])
				}
			}

			//fmt.Println(row[54], row[56], row[58], row[60], row[62])
		}
	}
}
