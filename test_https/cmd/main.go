package main

import (
	"crypto/tls"
	"flag"
	"fmt"
	"io"
	"net/http"
	"net/http/cookiejar"
	"os"
	"time"

	"golang.org/x/net/publicsuffix"
)

var (
	DefaultRedirectLimit       = 5
	DefaultClientTimeout       = time.Second * 10
	DefaultMaxIdleConns        = 32
	DefaultIdleConnTimeout     = time.Second * 60
	DefaultMaxConnsPerHost     = 128
	DefaultMaxIdleConnsPerHost = 32
)

func NewClient(skipVerify bool) *http.Client {
	var tlsconf = tls.Config{
		InsecureSkipVerify: skipVerify,
	}

	var transport = http.Transport{
		MaxIdleConns:        DefaultMaxIdleConns,
		IdleConnTimeout:     DefaultIdleConnTimeout,
		MaxConnsPerHost:     DefaultMaxConnsPerHost,
		MaxIdleConnsPerHost: DefaultMaxIdleConnsPerHost,
		TLSClientConfig:     &tlsconf,
	}

	return &http.Client{
		Timeout:       DefaultClientTimeout,
		Transport:     &transport,
		CheckRedirect: DefaultRedirectChecker,
	}
}

func DefaultRedirectChecker(req *http.Request, via []*http.Request) error {
	if len(via) >= DefaultRedirectLimit {
		return fmt.Errorf("stop after %d redirects", DefaultRedirectLimit)
	}

	fmt.Printf("Redirect to: %s\n", req.URL)
	return nil
}

func PrintTLS(state *tls.ConnectionState) {
	fmt.Printf("TLS.NegotiatedProtocol: \"%s\"\n", state.NegotiatedProtocol)

	switch state.Version {
	case tls.VersionTLS10:
		fmt.Printf("TLS.Version: 1.0\n")
	case tls.VersionTLS11:
		fmt.Printf("TLS.Version: 1.1\n")
	case tls.VersionTLS12:
		fmt.Printf("TLS.Version: 1.2\n")
	case tls.VersionTLS13:
		fmt.Printf("TLS.Version: 1.3\n")
	}

	for _, cert := range state.PeerCertificates {
		fmt.Printf("\nSerialNumber: %d\n", cert.SerialNumber)
		fmt.Printf("CommonName: %s\n", cert.Issuer.CommonName)
		fmt.Printf("NotBefore: %s\n", cert.NotBefore)
		fmt.Printf("NotAfter: %s\n", cert.NotAfter)

		if len(cert.DNSNames) > 0 {
			fmt.Fprintf(os.Stdout, "DNSNames: [\n")
			for _, dnsName := range cert.DNSNames {
				fmt.Printf("%s\n", dnsName)
			}
			fmt.Printf("]\n")
		}

		if len(cert.EmailAddresses) > 0 {
			fmt.Printf("EmailAddresses: [\n")
			for _, email := range cert.EmailAddresses {
				fmt.Printf("%s\n", email)
			}
			fmt.Printf("]\n")
		}

		if len(cert.IPAddresses) > 0 {
			fmt.Printf("IPAddresses: [\n")
			for _, ipAddr := range cert.IPAddresses {
				fmt.Printf("%s\n", ipAddr)
			}
			fmt.Printf("]\n")
		}
	}
}

func main() {
	var target = flag.String("url", "", "")
	var showBody = flag.Bool("body", false, "")
	var showHeaders = flag.Bool("headers", false, "")
	flag.Parse()

	if req, err := http.NewRequest(http.MethodGet, *target, nil); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)

	} else {
		var client = NewClient(true)

		if cookie, err := cookiejar.New(&cookiejar.Options{PublicSuffixList: publicsuffix.List}); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)

		} else {
			client.Jar = cookie
		}

		if resp, err := client.Do(req); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)

		} else {
			defer resp.Body.Close()
			fmt.Printf("%d - %s %s\n", resp.StatusCode, resp.Request.Method, resp.Request.URL)

			if *showHeaders {
				fmt.Printf("\n")
				for key := range resp.Header {
					fmt.Printf("%s: %s\n", key, resp.Header.Get(key))
				}
				fmt.Printf("\n")
			}

			if *showBody {
				fmt.Printf("Body:\n")
				if _, err := io.Copy(os.Stdout, resp.Body); err != nil {
					fmt.Fprintf(os.Stderr, "Error: %v\n", err)

				} else {
					fmt.Printf("\n\n")
				}
			}

			if resp.TLS != nil {
				PrintTLS(resp.TLS)
			}
		}
	}
}
