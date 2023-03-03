import requests
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--token", type=str)
parser.add_argument("-o", "--owner", type=str)
parser.add_argument("-r", "--repo", type=str)
parser.add_argument("-f", "--file", type=str)
parser.add_argument("-s", "--search", type=str)

args = parser.parse_args()

# Set the Github repository details
access_token = args.token
repo_owner = args.owner
repo_name = args.repo
file_path = args.file
search_phrase = args.search


# set up paging
per_page = 100
page = 0
count = 0

# Fetch the commit history of the file
headers = {
		"Accept": "application/vnd.github.v3+json",
		"Authorization": f"Bearer {access_token}",
		"X-GitHub-Api-Version": "2022-11-28"
}

# loop through urls until we get a 404
while True:
		page += 1
		url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?path={file_path}&per_page={per_page}&page={page}"
		response = requests.get(url, headers=headers)
		commits = json.loads(response.text)
		if response.status_code != 200 or len(commits) == 0:
				print(" Done")
				break

		# Search for the phrase in each commit message
		for commit in commits:
				commit_url = commit["url"]

				commit_response = requests.get(commit_url, headers=headers)
				commit_data = json.loads(commit_response.text)
				for file in commit_data["files"]:
						if file["filename"] == file_path:
								patch = file["patch"]
								count += 1
								commit_date = commit_data["commit"]["author"]["date"] 
								print(f"[{count}]", end='\r')
								if search_phrase in patch:
										print(f"[{count}] Found it! {commit_date} https://github.com/{repo_owner}/{repo_name}/commit/{commit_data['sha']}\r")

