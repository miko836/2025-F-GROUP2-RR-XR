import json
import requests
import csv
import os

if not os.path.exists("data"):
    os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttokens, ct):
    jsonData = None
    try:
        ct = ct % len(lsttokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttokens[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        print("Auth error:", e)
    return jsonData, ct

# @dictFiles: dictionary that stores file → [(author, date), ...]
# @lstTokens: GitHub authentication tokens
# @repo: GitHub repo name (e.g., "owner/repo")
def collect_file_touches(dictfiles, lsttokens, repo):
    ipage = 1  # commit pages
    ct = 0  # token counter

    try:
        while True:
            spage = str(ipage)
            commitsUrl = f'https://api.github.com/repos/{repo}/commits?page={spage}&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            if not jsonCommits or len(jsonCommits) == 0:
                break  # no more commits

            for shaObject in jsonCommits:
                sha = shaObject['sha']
                shaUrl = f'https://api.github.com/repos/{repo}/commits/{sha}'
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)

                if not shaDetails:
                    continue

                commit_author = shaDetails["commit"]["author"]["name"]
                commit_date = shaDetails["commit"]["author"]["date"][:10]  # YYYY-MM-DD

                if "files" not in shaDetails:
                    continue

                for filenameObj in shaDetails["files"]:
                    filename = filenameObj['filename']
                    
                    # Track author + date touches
                    if filename not in dictfiles:
                        dictfiles[filename] = []
                    dictfiles[filename].append((commit_author, commit_date))

                    print(f"{filename} touched by {commit_author} on {commit_date}")
            ipage += 1

    except Exception as e:
        print("Error receiving data:", e)
        exit(0)


# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack'
# repo = 'k9mail/k-9'
# repo = 'mendhak/gpslogger'

# Put your tokens here
lstTokens = ["5564"]

dictfiles = dict()
collect_file_touches(dictfiles, lstTokens, repo)
print('Total number of files: ' + str(len(dictfiles)))

file = repo.split('/')[1]
fileOutput = 'data/file_' + file + '_authors.csv'

with open(fileOutput, 'w', newline='', encoding="utf-8") as fileCSV:
    writer = csv.writer(fileCSV)
    writer.writerow(["Filename", "Author", "Date"])
    
    for filename, touches in dictfiles.items():
        for author, date in touches:
            writer.writerow([filename, author, date])

print(f"Saved detailed author touches to {fileOutput}")
