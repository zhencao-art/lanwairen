package main

import (
    "image"
    "image/color"
    "image/jpeg"
//    "io"
    //"math"
    "os"
    "log"
)

const (
    dx = 500
    dy = 500
)

func main() {
    file, err := os.Create("sinfun.jpeg")
    if err != nil {
        log.Fatal(err)
    }
    defer file.Close()
    alpha := image.NewAlpha(image.Rect(0,0,dx,dy))

    for i := 0; i < dx; i++ {
        for j := 0; j < dy; j++ {
            if j == i || (dx - j) == i {
                alpha.Set(i,j,color.Alpha{0})
            } else {
                alpha.Set(i,j,color.Alpha{255})
            }
        }
    }
    jpeg.Encode(file,alpha,nil)
}
