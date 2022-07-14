package reseputil

import (
	"github.com/xuri/excelize/v2"
	"log"
	"os"
	"strconv"
	"strings"
)

/*
Fungsi MappingResep berfungsi untuk me-return map[int]interface{} (kalau di python dictionary)
berisi data yang akan dimasukkan ke dalam faskes_emu. Map hanya berisi pasien yang mendapatkan
resep / obat. Pasien yang tidak mendapat resep / obat akan tercatat di file info.log
*/
func MappingResep() map[int]interface{} {
	file_log, err := os.OpenFile("info.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Println(err)
	}
	defer file_log.Close()

	logger := log.New(file_log, "", log.LstdFlags)

	f, err := excelize.OpenFile("Laporan Harian - Pelayanan Pasien.xlsx")
	if err != nil {
		logger.Fatal(err)
	}
	defer func() {
		if err := f.Close(); err != nil {
			logger.Println(err)
		}
	}()

	// Get all the rows in the Sheet1.
	rows, err := f.GetRows("Sheet1")
	if err != nil {
		logger.Println(err)
	}

	jml_row_valid := 0
	jml_row_no_valid := 0
	data_map := make(map[int]interface{})

	logger.Printf("================= PASIEN TANPA RESEP =================")
	for index, item := range rows {
		if index >= 25 {

			obat, signa, jml := ObatRegex(item[65]), SignaRegex(item[65]), JumlahObatRegex(item[65])
			lama_hari := HitungLamaPengobatan(jml, signa)

			if len(obat) > 0 {
				i, _ := strconv.Atoi(item[0])
				tgl_berobat := strings.Split(item[1], " ")
				diagnosa := []string{item[54], item[56], item[58], item[60], item[62]}
				data_map[i] = map[string]interface{}{
					"nama":            item[2],
					"no_kartu":        getNoKartu(item[4]),
					"alamat":          checkAlamat(item[14]),
					"tgl_lahir":       checkTglLahir(item[16]),
					"no_tlp":          getNoTelepon(item[8]),
					"tgl_berobat":     tgl_berobat[0],
					"diagnosa":        popEmptySlice(diagnosa),
					"nama_dokter":     item[26],
					"obat":            obat,
					"signa":           signa,
					"jml":             jml,
					"lama_pengobatan": lama_hari,
				}

				jml_row_valid += 1
			} else {
				logger.Printf("%s | Tgl: %s", item[2], strings.Split(item[1], " ")[0])
				jml_row_no_valid += 1
			}

		}
	}
	//fmt.Println(data_map)
	logger.Printf(`====================== SUMMARY ======================
	                Jml Input: %d. Tanpa R/: %d`, jml_row_valid, jml_row_no_valid)
	logger.Printf(`==================== MULAI SESI =====================`)
	return data_map

}

func popEmptySlice(s []string) []string {
	el := []string{}

	for _, item := range s {
		if item != "" {
			el = append(el, item)
		}
	}
	return el
}

func checkAlamat(s string) string {
	if s != "" {
		return s
	} else {
		return "BELUM DIKETAHUI"
	}
}

func checkTglLahir(s string) string {
	if s != "" {
		return s
	} else {
		return "1920-01-01"
	}
}

func getNoKartu(nik string) string {
	if nik != "" {
		return nik
	} else {
		return "belum_ada"
	}
}

func getNoTelepon(tlp string) string {
	if tlp != "" {
		return tlp
	} else {
		return "000"
	}
}
