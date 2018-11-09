package main

import (
	"bufio"
	"os"
	"strings"
)

func parseCSV(file *os.File) *[]byte {
	var firstLine string
	var newFileContent []string
	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)
	// Use this loop to get the first line of the file which contains the column names
	for scanner.Scan() {
		firstLine = scanner.Text()
		break
	}
	// Extract the column names from the start of the file
	columnNames := strings.Split(strings.Replace(firstLine, "\n", "", 1), ",")
	// Find the indexes of the columns to be deleted
	indexes := findIndexForColumn(columnNames, *columnsToDelete)
	removedColumnNames := removeColumnNames(firstLine, *indexes)
	newFileContent = append(newFileContent, removedColumnNames)
	for scanner.Scan() {
		line := strings.Split(scanner.Text(), *delimiter)
		// used to keep track of the original index when values are being deleted
		deleteOffset := 0
		for index := range line {
			for _, deleteIndex := range *indexes {
				if index == deleteIndex-deleteOffset {
					line = append(line[:index], line[index+1:]...)
					deleteOffset++
				}
			}
		}
		newLine := strings.Join(line, ",")
		newFileContent = append(newFileContent, newLine)
	}
	newFileString := []byte(strings.Join(newFileContent, "\n"))
	return &newFileString
}

// compares the column names we know we want to delete to all of the column names
// we push the index of the column names we want to delete to remove the value at that index later on
func findIndexForColumn(csvColumnNames []string, columnsToDelete string) *[]int {
	var indexes []int
	columns := strings.Split(columnsToDelete, ",")
	for index, csvColumnName := range csvColumnNames {
		for _, column := range columns {
			if csvColumnName == column {
				indexes = append(indexes, index)
			}
		}
	}
	return &indexes
}

// removes the to be deleted column names from the first line of the CSV file
func removeColumnNames(firstLine string, indexes []int) string {
	columnNames := strings.Split(firstLine, ",")
	deleteOffset := 0
	for index := range columnNames {
		for _, indexValue := range indexes {
			if index == indexValue-deleteOffset {
				columnNames = append(columnNames[:index], columnNames[index+1:]...)
				deleteOffset++
			}
		}
	}
	removedColumnNames := strings.Join(columnNames, ",")
	return removedColumnNames
}
