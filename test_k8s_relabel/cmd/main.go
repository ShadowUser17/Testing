package main

import (
	"context"
	"fmt"
	"os"
	"path/filepath"

	meta "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/clientcmd"
	"k8s.io/client-go/util/homedir"
	"k8s.io/client-go/util/retry"
)

func main() {
	var (
		kubeconfig = filepath.Join(homedir.HomeDir(), ".kube", "config")
		config     *rest.Config
		clientset  *kubernetes.Clientset
		err        error
	)

	if _, err := os.Stat(kubeconfig); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}

	if config, err = clientcmd.BuildConfigFromFlags("", kubeconfig); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}

	if clientset, err = kubernetes.NewForConfig(config); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}

	var deploymentsClient = clientset.AppsV1().Deployments("whoami")
	err = retry.RetryOnConflict(retry.DefaultRetry, func() error {
		if item, err := deploymentsClient.Get(context.TODO(), "whoami", meta.GetOptions{}); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			return err

		} else {
			fmt.Fprintf(os.Stdout, "Labels:\n")
			for key := range item.Spec.Template.Labels {
				fmt.Fprintf(os.Stdout, "%s: %s\n", key, item.Spec.Template.Labels[key])
			}

			if item.Spec.Template.Annotations != nil {
				fmt.Fprintf(os.Stdout, "Annotations:\n")
				for key := range item.Spec.Template.Annotations {
					fmt.Fprintf(os.Stdout, "%s: %s\n", key, item.Spec.Template.Annotations[key])
				}
			}

			if item.Spec.Template.Annotations == nil {
				item.Spec.Template.Annotations = make(map[string]string)
			}

			item.Spec.Template.Annotations["prometheus.io/scrape"] = "\"true\""
			item.Spec.Template.Annotations["prometheus.io/port"] = "\"4000\""
			item.Spec.Template.Annotations["prometheus.io/path"] = "\"/prometheus/\""

			_, err = deploymentsClient.Update(context.TODO(), item, meta.UpdateOptions{})
			return err
		}
	})

	if err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
}
