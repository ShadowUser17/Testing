package main

import (
	"crypto/tls"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"time"
)

type Annotations struct {
	Fingerprint string `json:"fingerprint"`
	Description string `json:"description"`
	Dashboard   string `json:"dashboard"`
	Summary     string `json:"summary"`
	Docs        string `json:"docs"`
}

func (self *Annotations) String() string {
	return fmt.Sprintln(
		"Fingerprint: "+self.Fingerprint,
		"\nSummary: "+self.Summary,
		"\nDescription: "+self.Description,
		"\nDashboard: "+self.Dashboard,
		"\nDocs: "+self.Docs,
	)
}

type Labels struct {
	Alertname string `json:"alertname"`
	Severity  string `json:"severity"`
}

func (self *Labels) String() string {
	return fmt.Sprintln(
		"Alertname: "+self.Alertname,
		"\nSeverity: "+self.Severity,
	)
}

type Alert struct {
	Annotations Annotations `json:"annotations"`
	Labels      Labels      `json:"labels"`
}

func (self *Alert) String() string {
	return fmt.Sprint(
		self.Labels.String(),
		self.Annotations.String(),
	)
}

func NewClient() *http.Client {
	var tlsconf = tls.Config{
		InsecureSkipVerify: true,
	}

	var transport = http.Transport{
		TLSClientConfig: &tlsconf,
	}

	return &http.Client{
		Timeout:   time.Second * 10,
		Transport: &transport,
	}
}

func GetJsonDecoder(resp *http.Response) *json.Decoder {
	return json.NewDecoder(resp.Body)
}

func main() {
	var client = NewClient()

	if resp, err := client.Get("http://127.0.0.1:9093/api/v2/alerts"); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)

	} else {
		defer resp.Body.Close()
		var decoder = GetJsonDecoder(resp)
		var alerts []Alert

		if err = decoder.Decode(&alerts); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)

		} else {
			fmt.Printf("Received %d alerts from %s\n\n", len(alerts), resp.Request.URL)
			for _, item := range alerts {
				fmt.Println(item.String())
			}
		}
	}
}
