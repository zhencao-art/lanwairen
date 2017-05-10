package main

import("../common"
       "fmt")

func main() {
    items := [...]int{1,2,3}
    total := common.Sum(items)
    fmt.Print("%v",total);
}
