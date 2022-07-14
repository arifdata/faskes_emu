package restauto

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
	NamaBarang    int     `json:"nama_barang"`
	Jumlah        int     `json:"jumlah"`
	TglKadaluarsa *string `json:"tgl_kadaluarsa"`
	NoBatch       string  `json:"no_batch"`
}

type BukuPenerimaan struct {
	TanggalTerima string       `json:"tgl_terima"`
	Sumber        int          `json:"sumber"`
	Notes         string       `json:"notes"`
	PenerimaanSet []Penerimaan `json:"penerimaan_set"`
}

type Diagnosa struct {
	Diagnosa string `json:"diagnosa"`
}

func (Diagnosa) TableName() string {
	return "poli_diagnosa"
}
