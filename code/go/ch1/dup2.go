package main

import (
    "bufio"
    "fmt"
    "os"
)

func main() {
    count := make(map[string]int)
    files := os.Args[1:]

    if len(files) != 0 {
        for _, file := range files {
            f, err := os.Open(file)
            if err != nil {
                fmt.Fprintf(os.Stderr,"open file %s failed",file)
                continue
            }
            countlines(f,count)
            f.Close()
        }
        for line, n := range count {
            fmt.Printf("[%s]=%d\n",line,n)
        }
    }
}

func countlines(f *os.File,count map[string]int) {
    scanner := bufio.NewScanner(f)
    for scanner.Scan() {
        count[scanner.Text()] = count[scanner.Text()] + 1
    }
}
