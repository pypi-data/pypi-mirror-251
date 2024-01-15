from zenyx import printf
import requests
import os

def get_latest_release_tag(repo_owner, repo_name):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(api_url)

    if response.status_code != 200:
        print(
            f"Failed to retrieve latest release information. Status code: {response.status_code}"
        )
        return None

    release_info = response.json()
    return release_info["tag_name"]


def download_url(url, save_path, chunk_size=128):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)


def get_github_release(repo_owner, repo_name, download_path="."):
    latest_release_tag = get_latest_release_tag(repo_owner, repo_name)

    if not latest_release_tag:
        return

    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/tags/{latest_release_tag}"
    response = requests.get(api_url)

    if response.status_code != 200:
        printf(
            f"  @!Kotlyn$&/download_github_release",
            "@!Failed to retrieve release information. Status code: {response.status_code}$&",
            sep="\n",
        )
    release_info = response.json()
    assets = release_info["assets"]

    for asset in assets:
        asset_url = asset["browser_download_url"]
        asset_name = asset["name"]
        download_url(asset_url, os.path.join(download_path, asset_name))

    printf(
        f"  @!Kotlyn$&/download_github_release",
        "   @~Latest release ({latest_release_tag}) downloaded successfully.$&",
        sep="\n",
    )