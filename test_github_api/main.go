package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"net/http"
)

type Repo struct {
	Name   string `json:"name"`
	Branch string `json:"default_branch"`
	Type   string `json:"visibility"`
	Ssh    string `json:"ssh_url"`
	Http   string `json:"url"`
	Fork   bool   `json:"fork"`
}

func (repo *Repo) String() string {
	return fmt.Sprintln(
		repo.Name,
		repo.Type,
		repo.Branch,
		repo.Http,
		repo.Ssh,
		repo.Fork,
	)
}

func main() {
	var (
		gitUser  = flag.String("u", "", "Set Github user.")
		gitToken = flag.String("t", "", "Set Github token.")
	)

	flag.Parse()

	if data, err := getRepos(*gitUser, *gitToken); err != nil {
		fmt.Printf("Error: %v\n", err)
	} else {
		for index := range data {
			if data[index].Fork {
				fmt.Println(data[index])
			}
		}
	}
}

func getRepos(userName string, authToken string) ([]Repo, error) {
	var (
		err error
		req *http.Request
		rsp *http.Response
	)

	if req, err = http.NewRequest(http.MethodGet, "https://api.github.com/users/"+userName+"/repos", nil); err != nil {
		return nil, err
	}

	req.Header.Add("Accept", "application/vnd.github+json")
	req.Header.Add("X-GitHub-Api-Version", "2022-11-28")
	req.Header.Add("Authorization", "Bearer "+authToken)

	if rsp, err = http.DefaultClient.Do(req); err != nil {
		return nil, err
	} else {
		defer rsp.Body.Close()

		var decoder = json.NewDecoder(rsp.Body)
		var data = make([]Repo, 0)
		return data, decoder.Decode(&data)
	}
}
