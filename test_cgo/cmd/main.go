package main

/*
#include <stdlib.h>
*/
import "C"

import (
	"fmt"
	"time"
)

func main() {
	var now = time.Now()
	C.srand(C.uint(now.UnixNano()))
	fmt.Printf("Number: %d\n", int(C.random()))
}
