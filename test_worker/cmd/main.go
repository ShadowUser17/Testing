package main

import (
	"log"
	"math/rand"
	"sync"
	"time"
)

var (
	interval = time.NewTicker(time.Second * 1)
	timer    = time.NewTimer(time.Second * 5)
	group    = new(sync.WaitGroup)
	data     chan int
	exit     chan bool
)

func main() {
	data = make(chan int)
	exit = make(chan bool)

	group.Add(1)
	go sender()

	group.Add(1)
	go receiver()

	group.Add(1)
	go closer()

	group.Wait()
}

func sender() {
	var tmp int

	for {
		select {
		case <-exit:
			log.Printf("Sender: exit")
			close(data)
			group.Done()
			return

		case <-interval.C:
			tmp = rand.Int()
			log.Printf("Sender: set %d", tmp)
			data <- tmp
		}
	}
}

func receiver() {
	for tmp := range data {
		log.Printf("Receiver: get %d", tmp)
	}

	log.Printf("Receiver: exit")
	group.Done()
}

func closer() {
	<-timer.C
	log.Printf("Closer: set true")
	exit <- true

	log.Printf("Closer: exit")
	close(exit)
	group.Done()
}
