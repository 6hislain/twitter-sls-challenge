package main

import (
	"bufio"
	"bytes"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
)

func main() {
	filename := "./query2_ref.txt"
	folder := "./data"

	data, err := os.ReadFile(filename)
	if err != nil {
		fmt.Println("Error reading file:", err)
		return
	}

	lines := len(bytes.SplitAfter(data, []byte("\n")))

	numFiles := lines / 10
	if lines%10 > 0 {
		numFiles++
	}

	file, err := os.Open(filename)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)

	for i := 0; i < numFiles; i++ {
		outputFile := filepath.Join(folder, strconv.Itoa(i+1)+".json")

		outFile, err := os.Create(outputFile)
		if err != nil {
			fmt.Println("Error creating output file:", err)
			continue
		}
		defer outFile.Close()

		writer := bufio.NewWriter(outFile)

		lineCount := 0
		writer.WriteString("[")
		for scanner.Scan() && lineCount < 10 {
			line := scanner.Text() + "\n"
			_, err := writer.WriteString(line)
			if err != nil {
				fmt.Println("Error writing to file:", err)
				break
			}
			lineCount++
			if lineCount != 10 {
				writer.WriteString(",")
			}
		}
		writer.WriteString("]")

		err = writer.Flush()
		if err != nil {
			fmt.Println("Error flushing writer:", err)
			continue
		}
	}

	fmt.Printf("Successfully split %s into %d files in folder %s.\n", filename, numFiles, folder)
}
