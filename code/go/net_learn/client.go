package main

import (
    "fmt"
    "net"
    "time"
)

func main() {
    conn, err := net.Dial("tcp", "127.0.0.1:4199")
    if err != nil {
        fmt.Printf("conn server error\n")
        return
    }
    for {
        msg := []byte("echo test")
        conn.Write(msg)
        fmt.Printf("send msg %s\n", msg)
        time.Sleep(1000000000)
    }
}
