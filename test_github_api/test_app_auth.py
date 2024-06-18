#!/usr/bin/env python3
import os
import github
import pathlib
import datetime
import traceback


def get_app_client(app_id: int = 0, app_key: str = "") -> github.Github:
    app_id = int(os.environ.get("GITHUB_APP_ID", app_id))
    app_key_file = pathlib.Path(os.environ.get("GITHUB_APP_KEY", app_key))

    auth = github.Auth.AppAuth(app_id, app_key_file.read_text())
    git_integration = github.GithubIntegration(auth=auth)
    git_inst_id = git_integration.get_installations()[0].id

    auth = auth.get_installation_auth(git_inst_id)
    return github.Github(auth=auth)


try:
    now = datetime.datetime.now()
    client = get_app_client()

    github_org = os.environ.get("GITHUB_ORG")
    org = client.get_organization(github_org)
    print("Organization:", org.name)

    repo_list = org.get_repos(type="sources")
    print("Repositories:", repo_list.totalCount)
    for repo_item in repo_list:
        print("Repository:", repo_item.name)

        repo_runs = repo_item.get_workflow_runs(status="completed", created=now.strftime(r"%Y-%m-%d"))
        for run_item in repo_runs:
            print("\t\"{}\" \"{}\": {}".format(
                run_item.created_at.strftime(r"%Y-%m-%d %H:%M:%S"), run_item.name, run_item.status.capitalize()
            ))

except Exception:
    traceback.print_exc()
