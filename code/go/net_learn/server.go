package main

import (
    "fmt"
    "net"
)

func startEchoServer(address string) {
    ln, err := net.Listen("tcp", address)
    if err != nil {
        fmt.Printf("listen on %s error\n", address)
        return
    }
    for {
        conn, err := ln.Accept()
        fmt.Print("a new conn\n")
        if err != nil {
            fmt.Printf("accept error\n")
            return
        }
        go handleConnection(conn)
    }
}

func handleConnection(conn net.Conn) {
    fmt.Printf("handle conn\n")
    for {
        line := make([]byte, 128)
        rc, err := conn.Read(line)
        if err != nil {
            return
        }
        fmt.Printf("Get %s %d words\n", line, rc)
    }
}

func main() {
    startEchoServer("127.0.0.1:4199")
}
