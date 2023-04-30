package main_test

import (
	"io"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

func HttpHandler(response http.ResponseWriter, request *http.Request) {
	response.WriteHeader(http.StatusOK)
	response.Header().Set("Content-Type", "text/html")
	response.Write([]byte(time.Now().String()))
}

func TestExample(t *testing.T) {
	var mux = http.NewServeMux()
	mux.HandleFunc("/", HttpHandler)

	var server = httptest.NewServer(mux)
	defer server.Close()

	if resp, err := server.Client().Get(server.URL); err != nil {
		defer resp.Body.Close()
		t.Errorf("Get %s error: %v\n", server.URL, err)

	} else {
		defer resp.Body.Close()
		t.Logf("%s %s\n", server.URL, resp.Status)

		if data, err := io.ReadAll(resp.Body); err != nil {
			t.Errorf("Read body error: %v\n", err)

		} else {
			t.Logf("Data: %s\n", string(data))
		}
	}
}

func BenchmarkExample(b *testing.B) {
	var mux = http.NewServeMux()
	mux.HandleFunc("/", HttpHandler)

	var server = httptest.NewServer(mux)
	defer server.Close()

	for num := 0; num < b.N; num++ {
		if resp, err := server.Client().Get(server.URL); err != nil {
			defer resp.Body.Close()
			b.Errorf("Get %s error: %v\n", server.URL, err)

		} else {
			defer resp.Body.Close()
			if _, err := io.ReadAll(resp.Body); err != nil {
				b.Errorf("Read body error: %v\n", err)
			}
		}
	}
}
