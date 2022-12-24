package main

import (
	"context"
	"log"
	"os"
	"path/filepath"

	meta "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/tools/clientcmd"
	"k8s.io/client-go/util/homedir"
)

func main() {
	var (
		kubeconfig = filepath.Join(homedir.HomeDir(), ".kube", "config")
		logger     = log.New(os.Stdout, "", 0)
	)

	if _, err := os.Stat(kubeconfig); err != nil {
		logger.Fatalf("Error: %v\n", err)

	} else {
		if config, err := clientcmd.BuildConfigFromFlags("", kubeconfig); err != nil {
			logger.Fatalf("Error: %v\n", err)

		} else {
			if clientset, err := kubernetes.NewForConfig(config); err != nil {
				logger.Fatalf("Error: %v\n", err)

			} else {
				if ns, err := clientset.CoreV1().Namespaces().List(context.TODO(), meta.ListOptions{}); err != nil {
					logger.Fatalf("Error: %v\n", err)

				} else {
					for ns_index := range ns.Items {
						if pods, err := clientset.CoreV1().Pods(ns.Items[ns_index].Name).List(context.TODO(), meta.ListOptions{}); err != nil {
							logger.Fatalf("Error: %v\n", err)

						} else {
							if len(pods.Items) > 0 {
								logger.Printf("%s (%d):\n", ns.Items[ns_index].Name, len(pods.Items))
								for pod_index := range pods.Items {
									logger.Printf("\t%s\n", pods.Items[pod_index].Name)
								}
							}
						}
					}
				}
			}
		}
	}
}
