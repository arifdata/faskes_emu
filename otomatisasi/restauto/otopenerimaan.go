package restauto

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

type ApotekDataobat struct {
	ID           int    `gorm:"primary_key;AUTO_INCREMENT;column:id;type:integer;"`
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

type ApotekSumberterima struct {
	ID   int    `gorm:"primary_key;AUTO_INCREMENT;column:id;type:integer;"`
	Nama string `gorm:"column:nama;type:varchar;size:20;"`
}

func (ApotekSumberterima) TableName() string {
	return "apotek_sumberterima"
}

type Penerimaan struct {
	NamaBarang    int    `json:"nama_barang"`
	Jumlah        int    `json:"jumlah"`
	TglKadaluarsa string `json:"tgl_kadaluarsa"`
	NoBatch       string `json:"no_batch"`
}

type BukuPenerimaan struct {
	TanggalTerima string       `json:"tgl_terima"`
	Sumber        int          `json:"sumber"`
	Notes         string       `json:"notes"`
	PenerimaanSet []Penerimaan `json:"penerimaan_set"`
}

func Eksekusi() {
	/*
		data := &BukuPenerimaan{
			TanggalTerima: "2022-07-06",
			Sumber:        1,
			Notes:         "",
			PenerimaanSet: []Penerimaan{
				Penerimaan{
					NamaBarang: 7,
					Jumlah:     550,
				},
			},
		}
	*/

	data := &BukuPenerimaan{}
	data.PenerimaanSet = make([]Penerimaan, 2)
	data.TanggalTerima = "2022-07-11"
	data.Sumber = 1
	data.Notes = ""
	data.PenerimaanSet[0] = Penerimaan{
		NamaBarang:    7,
		Jumlah:        130,
		TglKadaluarsa: "2023-09-30",
		NoBatch:       "9878721",
	}
	data.PenerimaanSet[1] = Penerimaan{
		NamaBarang:    2,
		Jumlah:        10,
		TglKadaluarsa: "2024-07-12",
		NoBatch:       "126351",
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
