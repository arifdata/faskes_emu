package reseputil

import (
	"regexp"
	"strconv"
)

/*
Func HitungLamaPengobatan berfungsi untuk menghitung lama pengobatan (dalam satuan hari). Function ini memerlukan 2 argumen
hasil return func JumlahObatRegex dan func SignaRegex. Jika terjadi error divided by zero maka dianggap lama pengobatan 3 hari saja.
*/
func HitungLamaPengobatan(jml []int, signa []string) []int {
	re := regexp.MustCompile("\\d{1}")
	lama_pengobatan := []int{}

	for index, item := range jml {
		a := re.Find([]byte(signa[index]))
		angka_signa, _ := strconv.Atoi(string(a))
		if angka_signa != 0 && item != 1 {
			jml_hari := item / angka_signa
			lama_pengobatan = append(lama_pengobatan, jml_hari)
		} else if item == 1 {
			lama_pengobatan = append(lama_pengobatan, 3)
		} else {
			lama_pengobatan = append(lama_pengobatan, 3)
		}

	}
	return lama_pengobatan
}

/*
Func ObatRegex berfungsi untuk memecah string yang diperoleh dari kolom "Resep" pada laporan generated dari
https://bintan.epuskesmas.id/laporanpelayananpasien. Func ObatRegex ini memerlukan argumen tipe string dan
akan me-return slice of string. Contoh argumen string seperti berikut:

- Ibuprofen tablet 400 mg
  Signa : 3x1
  Jumlah : 10
  Racikan :

- Parasetamol tablet 500 mg
  Signa : 3x1
  Jumlah : 10
  Racikan :

- Vitamin B-Kompleks tablet
  Signa : 2x1
  Jumlah : 20
  Racikan :


akan me-return value sebagai berikut:

[]string{
	"Ibuprofen tablet 400 mg",
	"Parasetamol tablet 500 mg",
	"Vitamin B-Kompleks tablet",
}
*/
func ObatRegex(s string) []string {
	re := regexp.MustCompile("- (.*)\\w+")
	slice_obat := []string{}

	match := re.FindAll([]byte(s), -1)

	for _, obat := range match {
		s := regexp.MustCompile("- ").Split(string(obat), 2)
		slice_obat = append(slice_obat, s[1])

	}

	return slice_obat
}

/*
Func SignaRegex berfungsi untuk memecah string yang diperoleh dari kolom "Resep" pada laporan generated dari
https://bintan.epuskesmas.id/laporanpelayananpasien. Func SignaRegex ini memerlukan argumen tipe string dan
akan me-return slice of string. Contoh argumen string seperti berikut:

`- Ibuprofen tablet 400 mg
  Signa : 3x1
  Jumlah : 10
  Racikan :

- Parasetamol tablet 500 mg
  Signa : 3x1
  Jumlah : 10
  Racikan :

- Vitamin B-Kompleks tablet
  Signa : 2x1
  Jumlah : 20
  Racikan :`

akan me-return value sebagai berikut:
[]string{
	"3x1",
	"3x1",
	"2x1",
}
*/
func SignaRegex(s string) []string {
	re := regexp.MustCompile("Signa.*")
	slice_signa := []string{}

	match := re.FindAll([]byte(s), -1)

	for _, signa := range match {
		s := regexp.MustCompile(" : ").Split(string(signa), 2)
		slice_signa = append(slice_signa, s[1])

	}

	return slice_signa
}

/*
Func JumlahObatRegex berfungsi untuk memecah string yang diperoleh dari kolom "Resep" pada laporan generated dari
https://bintan.epuskesmas.id/laporanpelayananpasien. Func JumlahObatRegex ini memerlukan argumen tipe string dan
akan me-return slice of integer. Contoh argumen string seperti berikut:

`- Ibuprofen tablet 400 mg
  Signa : 3x1
  Jumlah : 10
  Racikan :

- Parasetamol tablet 500 mg
  Signa : 3x1
  Jumlah : 10
  Racikan :

- Vitamin B-Kompleks tablet
  Signa : 2x1
  Jumlah : 20
  Racikan :`

akan me-return value sebagai berikut:
[]int{
	10,
	10,
	20,
}
*/
func JumlahObatRegex(s string) []int {
	re := regexp.MustCompile("Jumlah.*")
	slice_jumlah := []int{}

	match := re.FindAll([]byte(s), -1)

	for _, jumlah := range match {
		s := regexp.MustCompile(" : ").Split(string(jumlah), 2)
		i, _ := strconv.Atoi(s[1])

		slice_jumlah = append(slice_jumlah, i)

	}

	return slice_jumlah
}
