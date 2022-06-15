package main

import (
	"fmt"
	_ "test_term_module/pkg/termcolor.v1"
	color "test_term_module/pkg/termcolor.v2"
)

func main() {
	var termColor = color.New(color.FgHiRed, color.Bold)
	fmt.Println(termColor.Set("Testing..."))
}
