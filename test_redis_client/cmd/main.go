package main

import (
	"context"
	"flag"
	"fmt"
	"os"

	"github.com/go-redis/redis/v8"
)

func main() {
	var (
		options = new(redis.Options)
		ctx     = context.Background()
	)

	flag.StringVar(&options.Addr, "s", "127.0.0.1:6379", "Set redis: address:port")
	flag.IntVar(&options.DB, "d", 0, "Set Redis DB")
	flag.StringVar(&options.Username, "u", "", "Set redis user")
	flag.StringVar(&options.Password, "p", "", "Set redis password")
	flag.Parse()

	fmt.Printf(
		"Redis: %s\nUser: %s\nPasswd: %s\nDB: %d\n",
		options.Addr, options.Username, options.Password, options.DB,
	)

	var client = redis.NewClient(options)

	if res, err := client.Keys(ctx, "*").Result(); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)

	} else {
		for index := range res {
			if ttl, err := client.TTL(ctx, res[index]).Result(); err == nil && ttl <= 0 {
				fmt.Printf("ID: %d Key: %s TTL: %d\n", index, res[index], ttl)
			}
		}
	}
}
