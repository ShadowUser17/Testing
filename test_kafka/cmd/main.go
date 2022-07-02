package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	"sync"
	"time"

	"github.com/confluentinc/confluent-kafka-go/kafka"
)

func main() {
	var (
		group  = new(sync.WaitGroup)
		config = kafka.ConfigMap{
			"bootstrap.servers": "127.0.0.1:9092",
			"client.id":         "test_worker",
			"acks":              "all",
		}
	)

	var ctx, exit = context.WithCancel(context.Background())

	group.Add(1)
	go exiter(group, ctx, exit)

	group.Add(1)
	go producer(group, ctx, exit, &config)

	group.Add(1)
	go consumer(group, ctx, exit, &config)

	group.Wait()
}

func producer(wg *sync.WaitGroup, ctx context.Context, exit context.CancelFunc, config *kafka.ConfigMap) {
	log.Println("Start producer")
	defer wg.Done()

	var topic = "testing"
	var delivery = make(chan kafka.Event, 500)
	defer close(delivery)

	var client, err = kafka.NewProducer(config)
	defer client.Close()

	if err != nil {
		log.Printf("Producer error: %v", err)
		exit()
		return
	}

	for {
		select {
		case <-ctx.Done():
			log.Println("Stop producer")
			return

		case event := <-delivery:
			if msg := event.(*kafka.Message); msg.TopicPartition.Error != nil {
				log.Printf("Delivery failed: %v", msg.TopicPartition.Error)

			} else {
				log.Printf(
					"Topic: %s Partition: %d Offset: %v",
					*msg.TopicPartition.Topic,
					msg.TopicPartition.Partition,
					msg.TopicPartition.Offset,
				)
			}

		default:
			err = client.Produce(
				&kafka.Message{
					TopicPartition: kafka.TopicPartition{
						Topic:     &topic,
						Partition: kafka.PartitionAny,
					},
					Value: []byte(time.Now().String()),
				},
				delivery,
			)

			if err != nil {
				log.Printf("Producer error: %v", err)
			}
		}
	}
}

func consumer(wg *sync.WaitGroup, ctx context.Context, exit context.CancelFunc, config *kafka.ConfigMap) {
	log.Println("Start consumer")
	defer wg.Done()

	var client, err = kafka.NewConsumer(config)
	defer client.Close()

	if err != nil {
		log.Printf("Consumer error: %v", err)
		exit()
		return
	}

	err = client.SubscribeTopics([]string{"testing"}, nil)
	if err != nil {
		log.Printf("Consumer error: %v", err)
		exit()
		return
	}

	for {
		select {
		case <-ctx.Done():
			log.Println("Stop consumer")
			return

		default:
			event := client.Poll(0)
			switch msg := event.(type) {
			case *kafka.Message:
				log.Printf(
					"Topic: %s Value: \"%s\"",
					msg.TopicPartition,
					string(msg.Value),
				)

			case kafka.Error:
				log.Printf("Consumer error: %v", msg)
				exit()
				return
			}
		}
	}
}

func exiter(wg *sync.WaitGroup, ctx context.Context, exit context.CancelFunc) {
	log.Println("Start exiter")
	defer wg.Done()

	var sigChan = make(chan os.Signal, 1)
	signal.Notify(sigChan)
	defer close(sigChan)

	for {
		select {
		case <-ctx.Done():
			log.Println("Stop exiter")
			return

		case <-sigChan:
			log.Println("Interrupt...")
			exit()
			return
		}
	}
}
