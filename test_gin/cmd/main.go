package main

import (
	"flag"
	"fmt"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
)

func main() {
	var address = flag.String("listen", ":8080", "Set address:port")
	flag.Parse()

	gin.SetMode(gin.ReleaseMode)
	var router = gin.New()

	router.Use(gin.LoggerWithFormatter(Formatter))
	router.GET("/", Handler)

	if err := router.Run(*address); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
}

func Handler(ctx *gin.Context) {
	ctx.JSON(http.StatusOK, gin.H{
		"request_proto":      ctx.Request.Proto,
		"request_method":     ctx.Request.Method,
		"request_path":       ctx.Request.URL.Path,
		"request_useragent":  ctx.Request.UserAgent(),
		"request_remoteaddr": ctx.Request.RemoteAddr,
	})
}

func Formatter(param gin.LogFormatterParams) string {
	return fmt.Sprintf(
		"[%s] %s -> %s %s %d %s\n",
		param.TimeStamp.Format(time.RFC1123),
		param.ClientIP,
		param.Method,
		param.Path,
		param.StatusCode,
		param.Latency,
	)
}
