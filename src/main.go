package main

import (
	"flag"
	"io/ioutil"
	"log"
	"os"
)

var (
	columnsToDelete = flag.String("columnsToDelete", "", "Columns you wish to delete from the CSV file, required")
	csv             = flag.String("csv", "", "CSV file, required")
	delimiter       = flag.String("delimiter", "", "delimiter used in the CSV, required")
)

func main() {
	flag.Parse()
	log.Println("INFO: If you are trying to enter multiple column names enter them as such: columnName,otherColumnName. Please do not add spaces between column names.")
	file, err := os.Open(*csv)
	defer file.Close()
	if err != nil {
		log.Fatalf("ERROR: Problem reading csv file. Error: %v", err)
	}
	newFileString := parseCSV(file)
	err = ioutil.WriteFile(*csv, *newFileString, 0644)
	if err != nil {
		log.Fatalf("ERROR: Problem writing new content to CSV file. Error: %v", err)
	}
}
