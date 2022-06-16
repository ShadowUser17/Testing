package cert

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"crypto/x509/pkix"
	"encoding/pem"
	"math/big"
	"net"
	"os"
	"path"
	"time"
)

func MakeCert(certPath, hostName string) (string, string, error) {
	var (
		privKey *rsa.PrivateKey
		err     error
	)

	certPath = path.Join(certPath, hostName)
	if err = os.MkdirAll(certPath, 0700); err != nil {
		return "", "", err
	}

	if privKey, err = rsa.GenerateKey(rand.Reader, 2048); err != nil {
		return "", "", err
	}

	var (
		notBefore         = time.Now()
		notAfter          = notBefore.Add(365 * 24 * time.Hour)
		serialNumberLimit = new(big.Int).Lsh(big.NewInt(1), 128)
		serialNumber      *big.Int
	)

	if serialNumber, err = rand.Int(rand.Reader, serialNumberLimit); err != nil {
		return "", "", err
	}

	var template = x509.Certificate{
		IsCA:         true,
		SerialNumber: serialNumber,
		Subject: pkix.Name{
			CommonName: "Testing",
		},
		NotBefore:             notBefore,
		NotAfter:              notAfter,
		KeyUsage:              x509.KeyUsageKeyEncipherment | x509.KeyUsageDigitalSignature | x509.KeyUsageCertSign,
		ExtKeyUsage:           []x509.ExtKeyUsage{x509.ExtKeyUsageServerAuth},
		BasicConstraintsValid: true,
	}

	if ipAddr := net.ParseIP(hostName); ipAddr != nil {
		template.IPAddresses = append(template.IPAddresses, ipAddr)

	} else {
		template.DNSNames = append(template.DNSNames, hostName)
	}

	var certDer []byte
	if certDer, err = x509.CreateCertificate(rand.Reader, &template, &template, &privKey.PublicKey, privKey); err != nil {
		return "", "", err
	}

	var certFilePath = path.Join(certPath, "cert.pem")
	if certFile, err := os.Create(certFilePath); err != nil {
		return "", "", err

	} else {
		pem.Encode(certFile, &pem.Block{Type: "CERTIFICATE", Bytes: certDer})
		certFile.Close()
	}

	var keyFilePath = path.Join(certPath, "cert.key")
	if keyFile, err := os.Create(keyFilePath); err != nil {
		return "", "", err

	} else {
		pem.Encode(keyFile, &pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(privKey)})
		keyFile.Close()
	}

	if err = os.Chmod(path.Join(certPath, "cert.key"), 0600); err != nil {
		return "", "", err
	}

	return certFilePath, keyFilePath, nil
}
