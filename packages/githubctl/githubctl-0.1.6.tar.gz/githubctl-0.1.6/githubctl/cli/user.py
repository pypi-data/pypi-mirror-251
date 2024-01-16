import typer

from githubctl.github import GitHubAPI
from githubctl.utils import print_beauty
from githubctl.options import OutputOption


user_app = typer.Typer()


@user_app.command(name="profile")
def profile(
    user: str = typer.Option(..., "--user", "-u", help="github user name"),
):
    """
    get user profile

    EXAMPLE

    githubctl user profile -u haoel
    """
    github_api = GitHubAPI()
    repo = github_api.get_all_repositories_for_user(username=user)
    followers = github_api.list_followers_of_user(username=user)
    following = github_api.list_people_user_follows(username=user)

    profile = {
        "repositories": len(repo) if repo else 0,
        "followers": len(followers) if followers else 0,
        "following": len(following) if following else 0,
    }
    print_beauty([profile], output=OutputOption.table)
