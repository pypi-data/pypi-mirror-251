import typer
import jmespath

from githubctl.options import OutputOption
from githubctl.github import GitHubAPI
from githubctl.utils import print_beauty, sort_by_key

repo_app = typer.Typer()


@repo_app.command(name="list")
def list_repos(
    user: str = typer.Option(..., "--user", "-u", help="github user name"),
    output: OutputOption = typer.Option(
        OutputOption.table, "--output", "-o", help="output format"
    ),
    query: str = typer.Option(None, "--query", "-q", help="query with jmespath"),
    sort_by: str = typer.Option(None, "--sort-by", "-s", help="sort by key"),
):
    """
    list all the repositories for a user.

    EXAMPLE

    githubctl repo list -u haoel --output=table --query="[?language=='Go']" --sort-by=~stars
    """
    github_api = GitHubAPI()
    repo = github_api.get_all_repositories_for_user(username=user)
    if query:
        repo = jmespath.search(query, repo)
    if sort_by:
        if sort_by.startswith("~"):
            reverse = True
            sort_by = sort_by[1:].split(",")
        else:
            reverse = False
        repo = sort_by_key(list_of_dict=repo, key_list=sort_by, reverse=reverse)
    print_beauty(list_of_dict=repo, output=output)


@repo_app.command(name="delete")
def delete_repo(
    user: str = typer.Option(..., "--user", "-u", help="github user name"),
    repo: str = typer.Option(..., "--repo", "-r", help="repo name"),
):
    """
    delete a user own repository

    EXAMPLE

    githubctl repo delete -u test -r test
    """
    github_api = GitHubAPI()
    if github_api.delete_repository_for_user(username=user, repo_name=repo):
        print(f"repository {repo} was deleted!")
    else:
        print(f"failed to delete repository {repo}")
