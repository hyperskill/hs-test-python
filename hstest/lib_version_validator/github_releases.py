import requests


class Author:
    def __init__(self, data: dict):
        self.login = data['login']
        self.id = data['id']
        self.node_id = data['node_id']
        self.avatar_url = data['avatar_url']
        self.gravatar_id = data['gravatar_id']
        self.url = data['url']
        self.html_url = data['html_url']
        self.followers_url = data['followers_url']
        self.following_url = data['following_url']
        self.gists_url = data['gists_url']
        self.starred_url = data['starred_url']
        self.subscriptions_url = data['subscriptions_url']
        self.organizations_url = data['organizations_url']
        self.repos_url = data['repos_url']
        self.events_url = data['events_url']
        self.received_events_url = data['received_events_url']
        self.type = data['type']
        self.site_admin = data['site_admin']

    def __str__(self):
        return f"Author({self.login}, {self.id})"


class Release:
    def __init__(self, data: dict):
        self.url = data['url']
        self.assets_url = data['assets_url']
        self.upload_url = data['upload_url']
        self.html_url = data['html_url']
        self.id = data['id']
        self.author = Author(data['author'])
        self.node_id = data['node_id']
        self.tag_name = data['tag_name']
        self.target_commitish = data['target_commitish']
        self.name = data['name']
        self.draft = data['draft']
        self.prerelease = data['prerelease']
        self.created_at = data['created_at']
        self.published_at = data['published_at']
        self.assets = data['assets']
        self.tarball_url = data['tarball_url']
        self.zipball_url = data['zipball_url']
        self.body = data['body']

    def __str__(self):
        return f"Release({self.name}, {self.tag_name}, {self.author})"


def get_latest_release() -> Release:
    url = f"https://api.github.com/repos/hyperskill/hs-test-python/releases/latest"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return Release(data)


if __name__ == "__main__":
    repo = "hyperskill/hs-test-python"
    latest_release = get_latest_release().tag_name
    print(latest_release)
