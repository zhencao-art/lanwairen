package main

import (
    "fmt"
    "os"
    "io/ioutil"
)

func main() {
    _, err := ioutil.TempDir(os.TempDir(), "somedata")
    if err != nil {
        fmt.Printf("%s", "create dir error")
        return
    }
    // defer os.RemoveAll(p)
}
