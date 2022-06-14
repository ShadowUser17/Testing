package termcolor

import (
	"os"
)

var (
	BgGreen   = string([]byte{27, 91, 57, 55, 59, 52, 50, 109})
	BgWhite   = string([]byte{27, 91, 57, 48, 59, 52, 55, 109})
	BgYellow  = string([]byte{27, 91, 57, 48, 59, 52, 51, 109})
	BgRed     = string([]byte{27, 91, 57, 55, 59, 52, 49, 109})
	BgBlue    = string([]byte{27, 91, 57, 55, 59, 52, 52, 109})
	BgMagenta = string([]byte{27, 91, 57, 55, 59, 52, 53, 109})
	BgCyan    = string([]byte{27, 91, 57, 55, 59, 52, 54, 109})
	FgGreen   = string([]byte{27, 91, 51, 50, 109})
	FgWhite   = string([]byte{27, 91, 51, 55, 109})
	FgYellow  = string([]byte{27, 91, 51, 51, 109})
	FgRed     = string([]byte{27, 91, 51, 49, 109})
	FgBlue    = string([]byte{27, 91, 51, 52, 109})
	FgMagenta = string([]byte{27, 91, 51, 53, 109})
	FgCyan    = string([]byte{27, 91, 51, 54, 109})
	Reset     = string([]byte{27, 91, 48, 109})
)

type Color struct {
	Background string
	Foreground string
}

func (color *Color) String() string {
	return color.Background + color.Foreground
}

func New(Background, Foreground string) *Color {
	return &Color{
		Background: Background,
		Foreground: Foreground,
	}
}

func Fprintln(out *os.File, color *Color, message string) (n int, err error) {
	if out == nil {
		out = os.Stdout
	}

	return out.WriteString(color.String() + message + "\n" + Reset)
}

func Println(color *Color, message string) (n int, err error) {
	return os.Stdout.WriteString(color.String() + message + "\n" + Reset)
}
