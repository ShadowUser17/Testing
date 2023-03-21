package main

import (
	"fmt"
	"os"
	"path/filepath"
	"time"

	v1 "k8s.io/api/core/v1"
	"k8s.io/client-go/informers"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/cache"
	"k8s.io/client-go/tools/clientcmd"
	"k8s.io/client-go/util/homedir"
)

func main() {
	var (
		kubeconfig      = filepath.Join(homedir.HomeDir(), ".kube", "config")
		config          *rest.Config
		clientset       *kubernetes.Clientset
		informerFactory informers.SharedInformerFactory
		stopFactory     = make(chan struct{})
		podInformer     cache.SharedIndexInformer
		err             error
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

	informerFactory = informers.NewSharedInformerFactory(clientset, time.Second*30)
	podInformer = informerFactory.Core().V1().Pods().Informer()
	podInformer.AddEventHandler(cache.ResourceEventHandlerFuncs{
		AddFunc: func(obj interface{}) {
			if pod, ok := obj.(*v1.Pod); ok {
				fmt.Printf("Added: %s/%s\n", pod.Namespace, pod.Name)
			}
		},
		DeleteFunc: func(obj interface{}) {
			if pod, ok := obj.(*v1.Pod); ok {
				fmt.Printf("Deleted: %s/%s\n", pod.Namespace, pod.Name)
			}
		},
		UpdateFunc: func(oldObj, newObj interface{}) {
			if pod, ok := oldObj.(*v1.Pod); ok {
				fmt.Printf("Deleted: %s/%s\n", pod.Namespace, pod.Name)
			}

			if pod, ok := newObj.(*v1.Pod); ok {
				fmt.Printf("Added: %s/%s\n", pod.Namespace, pod.Name)
			}
		},
	})

	informerFactory.Start(stopFactory)
	defer close(stopFactory)
	for {
		time.Sleep(time.Second)
	}
}
