package termcolorv2

import (
	"strconv"
	"strings"
)

// Base attributes
const (
	_ int = iota
	Bold
	Faint
	Italic
	Underline
	BlinkSlow
	BlinkRapid
	ReverseVideo
	Concealed
	CrossedOut
)

// Foreground colors
const (
	FgBlack int = iota + 30
	FgRed
	FgGreen
	FgYellow
	FgBlue
	FgMagenta
	FgCyan
	FgWhite
)

const (
	FgHiBlack int = iota + 90
	FgHiRed
	FgHiGreen
	FgHiYellow
	FgHiBlue
	FgHiMagenta
	FgHiCyan
	FgHiWhite
)

// Background colors
const (
	BgBlack int = iota + 40
	BgRed
	BgGreen
	BgYellow
	BgBlue
	BgMagenta
	BgCyan
	BgWhite
)

const (
	BgHiBlack int = iota + 100
	BgHiRed
	BgHiGreen
	BgHiYellow
	BgHiBlue
	BgHiMagenta
	BgHiCyan
	BgHiWhite
)

type Color struct {
	attrs string
}

func New(attrs ...int) *Color {
	var tmp = make([]string, len(attrs))

	for index, value := range attrs {
		tmp[index] = strconv.Itoa(value)
	}

	return &Color{
		attrs: "\033[" + strings.Join(tmp, ";") + "m",
	}
}

func (clr *Color) Set(text string) string {
	return clr.attrs + text + "\033[0m"
}
