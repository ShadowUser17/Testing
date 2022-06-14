package main

import (
	"test_term_module/pkg/termcolor"
)

func main() {
	var color = termcolor.New("", termcolor.FgRed)
	termcolor.Println(color, "Testing...")

	color.Foreground = termcolor.FgBlue
	termcolor.Println(color, "Testing...")

	color.Foreground = termcolor.FgYellow
	termcolor.Println(color, "Testing...")

	color.Foreground = termcolor.FgWhite
	termcolor.Println(color, "Testing...")

	color.Foreground = termcolor.FgCyan
	termcolor.Println(color, "Testing...")

	color.Foreground = termcolor.FgMagenta
	termcolor.Println(color, "Testing...")
}
