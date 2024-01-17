import os
import requests


class GitHubAPI:
    def __init__(self):
        if os.environ.get("GITHUB_TOKEN"):
            self.headers = {"Authorization": f"Bearer {os.environ.get('GITHUB_TOKEN')}"}
        else:
            self.headers = None

    def delete_repository_for_user(self, username, repo_name):
        """
        https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#delete-a-repository
        """
        base_url = f"https://api.github.com/repos/{username}/{repo_name}"
        response = requests.delete(base_url, headers=self.headers)
        if response.status_code == 204:
            return True
        else:
            return False

    def get_all_repositories_for_user(self, username):
        """
        https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#get-a-repository
        """
        base_url = f"https://api.github.com/users/{username}/repos"
        repos = []
        try:
            page = 1
            while True:
                params = {"page": page, "per_page": 100}  # Adjust per_page as needed
                response = requests.get(base_url, params=params, headers=self.headers)
                response.raise_for_status()

                repositories = response.json()
                if not repositories:
                    break  # No more repositories

                for repo in repositories:
                    repo_info = {
                        "id": repo["id"],
                        "name": repo["name"],
                        "url": repo["html_url"],
                        "description": repo["description"],
                        "language": repo["language"],
                        "stars": repo["stargazers_count"],
                        "forks": repo["forks_count"],
                        "fork": str(repo["fork"]),
                        "created_at": repo["created_at"],
                    }
                    repos.append(repo_info)

                page += 1

            return repos
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repositories for user {username}: {e}")
            return None

    def list_followers_of_user(self, username):
        base_url = f"https://api.github.com/users/{username}/followers"
        all_followers = []
        try:
            page = 1
            while True:
                params = {"page": page, "per_page": 100}  # Adjust per_page as needed
                response = requests.get(base_url, params=params, headers=self.headers)
                response.raise_for_status()

                followers = response.json()
                if not followers:
                    break

                for follower in followers:
                    all_followers.append(follower)

                page += 1

            return all_followers
        except requests.exceptions.RequestException as e:
            print(f"Error fetching followers for user {username}: {e}")
            return None

    def list_people_user_follows(self, username):
        base_url = f"https://api.github.com/users/{username}/following"
        all_following = []
        try:
            page = 1
            while True:
                params = {"page": page, "per_page": 100}  # Adjust per_page as needed
                response = requests.get(base_url, params=params, headers=self.headers)
                response.raise_for_status()

                following = response.json()
                if not following:
                    break

                for follow in following:
                    all_following.append(follow)

                page += 1

            return all_following
        except requests.exceptions.RequestException as e:
            print(f"Error fetching following for user {username}: {e}")
            return None
