package browserway

import (
	"fmt"
	"github.com/arifdata/faskes_emu/otomatisasi/reseputil"
	"github.com/go-rod/rod"
	"github.com/go-rod/rod/lib/launcher"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"
	"time"
)

func InputDataHarian() {
	// Aktivasi Logger
	file_log, err := os.OpenFile("info.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Println(err)
	}
	defer file_log.Close()
	logger := log.New(file_log, "", log.LstdFlags)

	u := launcher.New().Headless(false).MustLaunch()
	page := rod.New().Trace(true).SlowMotion(300 * time.Millisecond).ControlURL(u).MustConnect().MustPage("http://localhost:8000/app/login/?next=/app/").MustWindowMaximize()

	time.Sleep(3 * time.Second)

	// Proses Login
	page.MustElement("#id_username").MustInput("admin")
	page.MustElement("#id_password").MustInput("puskesmas")
	page.MustElement("#login-form > div.submit-row > input[type=submit]").MustClick()

	map_berobat := reseputil.MappingResep()
	keys := UrutkanKeys(map_berobat)

	fmt.Println(map_berobat, keys)
	logger.Printf("Mulai input.\n")

	for _, k := range keys {
		page.MustNavigate("http://localhost:8000/app/pendaftaran/datapasien/")
		search_input := strings.Join([]string{map_berobat[k].(map[string]interface{})["nama"].(string), map_berobat[k].(map[string]interface{})["no_kartu"].(string)}, " ")
		fmt.Println("Bersiap input", search_input)
		page.MustElement("#searchbar").MustInput(search_input)
		page.MustElement("#changelist-search > div > input[type=submit]:nth-child(3)").MustClick()
		adakahPasien := strings.Contains(page.MustElement("#changelist-form > p").MustHTML(), "0 Data Pasien")

		if !adakahPasien {
			// Menginput data berobat pasien
			page.MustElement("#nav-sidebar > div.app-poli.module > table > tbody > tr > td > a").MustClick()

			// Input nama pasien
			page.MustElement("#datakunjungan_form > div > fieldset:nth-child(1) > div.form-row.field-nama_pasien > div > div > span > span.selection > span > span.select2-selection__arrow > b").MustClick()
			page.MustElement("body > span > span > span.select2-search.select2-search--dropdown > input").MustInput(search_input)
			page.MustElement("#select2-id_nama_pasien-results").MustClick()
			// Input tanggal berobat
			page.MustElement("#id_tgl_kunjungan").MustInput(map_berobat[k].(map[string]interface{})["tgl_berobat"].(string))
			// Input penulis resep
			page.MustElement("#datakunjungan_form > div > fieldset:nth-child(2) > div.form-row.field-penulis_resep > div > div > span > span.selection > span > span.select2-selection__arrow > b").MustClick()
			page.MustElement("body > span > span > span.select2-search.select2-search--dropdown > input").MustInput(map_berobat[k].(map[string]interface{})["nama_dokter"].(string))
			page.MustElement("#select2-id_penulis_resep-results").MustClick()
			// Looping input diagnosa
			diagnosas := map_berobat[k].(map[string]interface{})["diagnosa"].([]string)
			for indexDiagnosa, diagnosa := range diagnosas {
				if indexDiagnosa == 0 {
					page.MustElement("#datakunjungan_form > div > fieldset:nth-child(2) > div.form-row.field-diagnosa > div > div > span > span.selection > span > ul > li > input").MustInput(diagnosa)
					page.MustElement("#select2-id_diagnosa-results").MustClick()

				} else {
					page.MustElement("#datakunjungan_form > div > fieldset:nth-child(2) > div.form-row.field-diagnosa > div > div > span > span.selection > span > ul > li.select2-search.select2-search--inline > input").MustInput(diagnosa)
					page.MustElement("#select2-id_diagnosa-results").MustClick()
				}

			}

			// Looping input obat, jumlah, signa, dan lama pengobatan
			obatObatan := map_berobat[k].(map[string]interface{})["obat"].([]string)
			jumlahObatObatan := map_berobat[k].(map[string]interface{})["jml"].([]int)
			signaObatObatan := map_berobat[k].(map[string]interface{})["signa"].([]string)
			lamaHariObatObatan := map_berobat[k].(map[string]interface{})["lama_pengobatan"].([]int)

			for index, obat := range obatObatan {
				if index > 4 {
					// Bila jumlah obat lebih dari 5
					page.MustElement("#resep_set-group > div > fieldset > table > tbody > tr.add-row > td > a").MustClick()
					page.MustElement(fmt.Sprintf("#resep_set-%d > td.field-nama_obat > div > span > span.selection > span > span.select2-selection__arrow > b", index)).MustClick()
					page.MustElement("body > span > span > span.select2-search.select2-search--dropdown > input").MustInput(obat)
					page.MustElement(fmt.Sprintf("#select2-id_resep_set-%d-nama_obat-results", index)).MustClick()

					// Input jumlah obat
					page.MustElement(fmt.Sprintf("#id_resep_set-%d-jumlah", index)).MustInput(strconv.Itoa(jumlahObatObatan[index]))

					// Input signa obat
					page.MustElement(fmt.Sprintf("#id_resep_set-%d-aturan_pakai", index)).MustInput(signaObatObatan[index])

					// Input lama hari pengobatan
					page.MustElement(fmt.Sprintf("#id_resep_set-%d-lama_pengobatan", index)).MustInput(strconv.Itoa(lamaHariObatObatan[index]))
				} else {
					// Bila jumlah obat antara 1 sampai 5
					// Input nama obat
					page.MustElement(fmt.Sprintf("#resep_set-%d > td.field-nama_obat > div > span > span.selection > span > span.select2-selection__arrow > b", index)).MustClick()
					page.MustElement("body > span > span > span.select2-search.select2-search--dropdown > input").MustInput(obat)
					page.MustElement(fmt.Sprintf("#select2-id_resep_set-%d-nama_obat-results", index)).MustClick()

					// Input jumlah obat
					page.MustElement(fmt.Sprintf("#id_resep_set-%d-jumlah", index)).MustInput(strconv.Itoa(jumlahObatObatan[index]))

					// Input signa obat
					page.MustElement(fmt.Sprintf("#id_resep_set-%d-aturan_pakai", index)).MustInput(signaObatObatan[index])

					// Input lama hari pengobatan
					page.MustElement(fmt.Sprintf("#id_resep_set-%d-lama_pengobatan", index)).MustInput(strconv.Itoa(lamaHariObatObatan[index]))
				}

			}
			// Submit button
			page.MustElement("#datakunjungan_form > div > div.submit-row > input.default").MustClick()

			//fmt.Println("Berhasil input", search_input)
			isBerhasilInput := strings.Contains(page.MustElement("#main > div").MustHTML(), "berhasil ditambahkan.")
			if isBerhasilInput {
				fmt.Println("Berhasil input", search_input)
				logger.Printf("%s | %s recorded.", search_input, map_berobat[k].(map[string]interface{})["tgl_berobat"].(string))
			} else {
				fmt.Println("Error: gagal input pada row", search_input)
				logger.Fatal("Data ", search_input, " gagal input.")
			}

		} else {
			// Menginput data pasien baru
			page.MustElement("#content-main > ul > li > a").MustClick()
			page.MustElement("#id_no_kartu").MustInput(map_berobat[k].(map[string]interface{})["no_kartu"].(string))
			page.MustElement("#id_nama_pasien").MustInput(map_berobat[k].(map[string]interface{})["nama"].(string))
			page.MustElement("#id_alamat").MustInput(map_berobat[k].(map[string]interface{})["alamat"].(string))
			page.MustElement("#id_usia").MustInput(map_berobat[k].(map[string]interface{})["tgl_lahir"].(string))
			page.MustElement("#id_no_hp").MustInput(map_berobat[k].(map[string]interface{})["no_tlp"].(string))
			page.MustElement("#datapasien_form > div > div > input.default").MustClick()
			logger.Printf("Pasien baru %s, alamat %s, no kartu %s sudah input.", map_berobat[k].(map[string]interface{})["nama"].(string), map_berobat[k].(map[string]interface{})["alamat"].(string), map_berobat[k].(map[string]interface{})["no_kartu"].(string))

			// Menginput data berobat pasien
			page.MustElement("#nav-sidebar > div.app-poli.module > table > tbody > tr > td > a").MustClick()

			// Input nama pasien
			page.MustElement("#datakunjungan_form > div > fieldset:nth-child(1) > div.form-row.field-nama_pasien > div > div > span > span.selection > span > span.select2-selection__arrow > b").MustClick()
			page.MustElement("body > span > span > span.select2-search.select2-search--dropdown > input").MustInput(search_input)
			page.MustElement("#select2-id_nama_pasien-results").MustClick()
			// Input tanggal berobat
			page.MustElement("#id_tgl_kunjungan").MustInput(map_berobat[k].(map[string]interface{})["tgl_berobat"].(string))
			// Input penulis resep
			page.MustElement("#datakunjungan_form > div > fieldset:nth-child(2) > div.form-row.field-penulis_resep > div > div > span > span.selection > span > span.select2-selection__arrow > b").MustClick()
			page.MustElement("body > span > span > span.select2-search.select2-search--dropdown > input").MustInput(map_berobat[k].(map[string]interface{})["nama_dokter"].(string))
			page.MustElement("#select2-id_penulis_resep-results").MustClick()
			// Looping input diagnosa
			diagnosas := map_berobat[k].(map[string]interface{})["diagnosa"].([]string)
			for indexDiagnosa, diagnosa := range diagnosas {
				if indexDiagnosa == 0 {
					page.MustElement("#datakunjungan_form > div > fieldset:nth-child(2) > div.form-row.field-diagnosa > div > div > span > span.selection > span > ul > li > input").MustInput(diagnosa)
					page.MustElement("#select2-id_diagnosa-results").MustClick()

				} else {
					page.MustElement("#datakunjungan_form > div > fieldset:nth-child(2) > div.form-row.field-diagnosa > div > div > span > span.selection > span > ul > li.select2-search.select2-search--inline > input").MustInput(diagnosa)
					page.MustElement("#select2-id_diagnosa-results").MustClick()
				}

			}

			// Looping input obat, jumlah, signa, dan lama pengobatan
			obatObatan := map_berobat[k].(map[string]interface{})["obat"].([]string)
			jumlahObatObatan := map_berobat[k].(map[string]interface{})["jml"].([]int)
			signaObatObatan := map_berobat[k].(map[string]interface{})["signa"].([]string)
			lamaHariObatObatan := map_berobat[k].(map[string]interface{})["lama_pengobatan"].([]int)

			for index, obat := range obatObatan {
				if index > 4 {
					// Bila jumlah obat lebih dari 5
					page.MustElement("#resep_set-group > div > fieldset > table > tbody > tr.add-row > td > a").MustClick()
					page.MustElement(fmt.Sprintf("#resep_set-%d > td.field-nama_obat > div > span > span.selection > span > span.select2-selection__arrow > b", index)).MustClick()
					page.MustElement("body > span > span > span.select2-search.select2-search--dropdown > input").MustInput(obat)
					page.MustElement(fmt.Sprintf("#select2-id_resep_set-%d-nama_obat-results", index)).MustClick()

					// Input jumlah obat
					page.MustElement(fmt.Sprintf("#id_resep_set-%d-jumlah", index)).MustInput(strconv.Itoa(jumlahObatObatan[index]))

					// Input signa obat
					page.MustElement(fmt.Sprintf("#id_resep_set-%d-aturan_pakai", index)).MustInput(signaObatObatan[index])

					// Input lama hari pengobatan
					page.MustElement(fmt.Sprintf("#id_resep_set-%d-lama_pengobatan", index)).MustInput(strconv.Itoa(lamaHariObatObatan[index]))
				} else {
					// Bila jumlah obat antara 1 sampai 5
					// Input nama obat
					page.MustElement(fmt.Sprintf("#resep_set-%d > td.field-nama_obat > div > span > span.selection > span > span.select2-selection__arrow > b", index)).MustClick()
					page.MustElement("body > span > span > span.select2-search.select2-search--dropdown > input").MustInput(obat)
					page.MustElement(fmt.Sprintf("#select2-id_resep_set-%d-nama_obat-results", index)).MustClick()

					// Input jumlah obat
					page.MustElement(fmt.Sprintf("#id_resep_set-%d-jumlah", index)).MustInput(strconv.Itoa(jumlahObatObatan[index]))

					// Input signa obat
					page.MustElement(fmt.Sprintf("#id_resep_set-%d-aturan_pakai", index)).MustInput(signaObatObatan[index])

					// Input lama hari pengobatan
					page.MustElement(fmt.Sprintf("#id_resep_set-%d-lama_pengobatan", index)).MustInput(strconv.Itoa(lamaHariObatObatan[index]))
				}

			}
			// Submit button
			page.MustElement("#datakunjungan_form > div > div.submit-row > input.default").MustClick()

			//fmt.Println("Berhasil input", search_input)
			isBerhasilInput := strings.Contains(page.MustElement("#main > div").MustHTML(), "berhasil ditambahkan.")
			if isBerhasilInput {
				fmt.Println("Berhasil input", search_input)
				logger.Printf("%s | %s recorded.", search_input, map_berobat[k].(map[string]interface{})["tgl_berobat"].(string))
			} else {
				fmt.Println("Error: gagal input pada row", search_input)
				logger.Fatal("Data ", search_input, " gagal input.")
			}

		}
		time.Sleep(3 * time.Second)

	}

	time.Sleep(time.Hour)

}

func UrutkanKeys(r map[int]interface{}) []int {
	keys := make([]int, 0, len(r))
	for key, _ := range r {
		keys = append(keys, key)
	}
	sort.Ints(keys)
	return keys
}
