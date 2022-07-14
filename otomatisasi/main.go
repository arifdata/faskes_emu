package main

import (
	"github.com/arifdata/faskes_emu/otomatisasi/browserway"
	"github.com/arifdata/faskes_emu/otomatisasi/restauto"
	"log"
	"os"
)

func main() {
	//restauto.InputBukuPenerimaan()
	//browserway.InputBukuPengeluaran()
	//restauto.InputDiagnosa()
	//browserway.InputDataHarian()

	argLength := len(os.Args[1:])

	if argLength > 0 {
		flag := os.Args[1]
		switch flag {
		case "diagnosa":
			restauto.InputDiagnosa()
		case "resep":
			browserway.InputDataHarian()
		case "penerimaan":
			restauto.InputBukuPenerimaan()
		case "pengeluaran":
			browserway.InputBukuPengeluaran()
		default:
			log.Fatal("Error! No such flag.")

		}
	} else {
		log.Fatal("No flag provided! Choose one: <diagnosa|resep|penerimaan|pengeluaran>")
	}

}
