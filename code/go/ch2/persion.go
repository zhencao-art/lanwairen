package main

import "fmt"

type talkInterface interface {
	talk(msg string)
}

type runInterface interface {
	run(length uint)
}

type Persion struct {
	name string
	age uint
}

func (p Persion) talk(msg string) {
	fmt.Printf("I am %s,What are you tablking about \"%s\"\n", p.name, msg)
}

func (p Persion) run(length uint) {
	fmt.Printf("I ran %v m\n", length)
}

func main() {
	ira := Persion{"ira.cao",10}
	ira.talk("Hello! Go world")
	ira.run(10)
}
