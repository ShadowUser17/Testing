package main_test

import (
	"fmt"
	"math/rand"
	"testing"
)

func TestExample(t *testing.T) {
	for num := 0; num < 5; num++ {
		t.Run(fmt.Sprintf("Test-%d", num), func(t *testing.T) {
			t.Parallel()
			t.Logf("Num: %d", rand.Intn(10))
		})
	}
}

/*func BenchmarkExample(b *testing.B) {
	for num := 0; num < b.N; num++ {

	}
}*/

/*func FuzzExample(f *testing.F) {

}*/
