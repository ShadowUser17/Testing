package types

import (
	"errors"
	"fmt"
	"time"
)

const (
	_ = iota
	REQ_OP_GET
)

type Time struct {
	Now time.Time
	Req int64
}

func (tm *Time) String() string {
	return fmt.Sprintf(
		"ID: %d Time: %s", tm.Req, tm.Now,
	)
}

func (tm *Time) Request(req int, replay *Time) error {
	tm.Req += 1
	tm.Now = time.Now()

	switch req {
	case REQ_OP_GET:
		replay.Req = tm.Req
		replay.Now = tm.Now
		return nil

	default:
		return errors.New("unsupported request code")
	}
}
