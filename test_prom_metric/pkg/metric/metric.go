package metric

import (
	"fmt"
	"strings"
	"sync"
)

type Metric struct {
	Tags  map[string]string
	Name  string
	Help  string
	Type  string
	value interface{}
	lock  *sync.Mutex
}

func New(name, help string) *Metric {
	return &Metric{
		Tags: make(map[string]string),
		Name: name,
		Help: help,
		Type: "gauge",
		lock: new(sync.Mutex),
	}
}

func (mtr *Metric) Set(value interface{}) {
	mtr.lock.Lock()
	mtr.value = value
	mtr.lock.Unlock()
}

func (mtr *Metric) String() string {
	mtr.lock.Lock()

	var header = fmt.Sprint(
		"# HELP ", mtr.Name, " ", mtr.Help, "\n",
		"# TYPE ", mtr.Name, " ", mtr.Type, "\n",
	)

	var tags = make([]string, 0)
	for key, val := range mtr.Tags {
		tags = append(tags, fmt.Sprint(key, "=\"", val, "\""))
	}

	var data = fmt.Sprint(
		header, mtr.Name, "{",
		strings.Join(tags, ","),
		"} ", mtr.value,
	)

	mtr.lock.Unlock()
	return data
}

func (mtr *Metric) Clear() {
	mtr.lock.Lock()

	mtr.value = nil
	for key := range mtr.Tags {
		mtr.Tags[key] = ""
	}

	mtr.lock.Unlock()
}
