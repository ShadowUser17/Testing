#!/usr/bin/env python3
import os
import github
import traceback


try:
    github_token = os.environ.get("GITHUB_TOKEN")
    github_org = os.environ.get("GITHUB_ORG")

    auth = github.Auth.Token(github_token)
    client = github.Github(auth=auth)

    org = client.get_organization(github_org)
    print("Organization:", org.name)

    repo_list = org.get_repos(type="sources")
    print("Repositories:", repo_list.totalCount)
    for repo_item in repo_list:
        print("Repository:", repo_item.name)

        repo_runs = repo_item.get_workflow_runs(status="queued")
        for run_item in repo_runs:
            print("\t{}: {}".format(run_item.name, run_item.status))

except Exception:
    traceback.print_exc()
