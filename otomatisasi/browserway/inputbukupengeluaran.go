package browserway

import (
	"fmt"
	"github.com/go-rod/rod"
	"github.com/go-rod/rod/lib/launcher"
	"github.com/xuri/excelize/v2"
	//"strconv"
	"time"
)

func InputBukuPengeluaran() {
	// buka file excel penerimaan_epus.xlsx pake excelize
	f, err := excelize.OpenFile("pengeluaran_epus.xlsx")
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

	u := launcher.New().Headless(false).MustLaunch()
	page := rod.New().Trace(true).SlowMotion(500 * time.Millisecond).ControlURL(u).MustConnect().MustPage("http://localhost:8000/app/login/?next=/app/").MustWindowMaximize()

	time.Sleep(3 * time.Second)

	// Proses Login
	page.MustElement("#id_username").MustInput("admin")
	page.MustElement("#id_password").MustInput("puskesmas")
	page.MustElement("#login-form > div.submit-row > input[type=submit]").MustClick()

	// Ke Menu Buku Pengeluaran
	page.MustElement("#content-main > div.app-apotek.module > table > tbody > tr.model-bukupengeluaran > th > a").MustClick()
	page.MustElement("#content-main > ul > li > a").MustClick()

	// Input Tanggal
	page.MustElement("#id_tgl_keluar").MustInput(rows[0][1])

	// Input Tujuan
	page.MustElement("#bukupengeluaran_form > div > fieldset > div.form-row.field-tujuan > div > div > span > span.selection > span > span.select2-selection__arrow > b").MustClick()
	page.MustElement("body > span > span > span.select2-search.select2-search--dropdown > input").MustInput(rows[0][3])
	page.MustElement("#select2-id_tujuan-results").MustClick()

	jmlRowObat := len(rows) - 4
	fmt.Println(jmlRowObat)

	for index, row := range rows {
		if index > 3 {
			if index-4 >= 5 {
				// handle item lebih dari 5
				page.MustElement("#pengeluaran_set-group > div > fieldset > table > tbody > tr.add-row > td > a").MustClick()

				page.MustElement(fmt.Sprintf("#pengeluaran_set-%d > td.field-nama_barang > div > span > span.selection > span > span.select2-selection__arrow > b", index-4)).MustClick()
				page.MustElement("body > span > span > span.select2-search.select2-search--dropdown > input").MustInput(row[2])
				page.MustElement(fmt.Sprintf("#select2-id_pengeluaran_set-%d-nama_barang-results", index-4)).MustClick()

				page.MustElement(fmt.Sprintf("#id_pengeluaran_set-%d-jumlah", index-4)).MustInput(row[10])

			} else {
				page.MustElement(fmt.Sprintf("#pengeluaran_set-%d > td.field-nama_barang > div > span > span.selection > span > span.select2-selection__arrow > b", index-4)).MustClick()
				page.MustElement("body > span > span > span.select2-search.select2-search--dropdown > input").MustInput(row[2])
				page.MustElement(fmt.Sprintf("#select2-id_pengeluaran_set-%d-nama_barang-results", index-4)).MustClick()

				page.MustElement(fmt.Sprintf("#id_pengeluaran_set-%d-jumlah", index-4)).MustInput(row[10])
			}
		}
	}

	page.MustElement("#bukupengeluaran_form > div > div.submit-row > input.default").MustClick()

	time.Sleep(time.Hour)
}
