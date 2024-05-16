package main

import (
	_ "context"
	_ "fmt"
	"os"

	"github.com/google/go-github/v62/github"
)

func main() {
	var (
		github_org   = os.Getenv("GITHUB_ORG")
		github_token = os.Getenv("GITHUB_TOKEN")
		//github_repos = []*github.Repository
	)

	var client = github.NewClient(nil).WithAuthToken(github_token)

	//client.Repositories.ListByOrg(context.Background(), github_org, nil)
}
