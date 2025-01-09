import argparse
import requests


def get_emails(username, token):
    base_url = "https://api.github.com/search/commits"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.cloak-preview"
    }

    emails = set()
    page = 1

    while True:
        params = {
            "q": f"author:{username}",
            "sort": "author-date",
            "order": "desc",
            "per_page": 100,
            "page": page
        }

        print(f"Fetching page {page}...")
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 403:
            print("Rate limit exceeded. Try again later.")
            break

        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            break

        data = response.json().get("items", [])
        if not data:
            print("No more pages to fetch.")
            break

        for commit in data:
            email = commit["commit"]["author"]["email"]
            repo = commit["repository"]["full_name"]
            print(f"Found email: {email} in {repo}")
            if "noreply.github.com" not in email:
                emails.add(email)

        print(f"Page {page} fetched, total emails found: {len(emails)}")
        page += 1

    return emails


def main():
    HARDCODED_TOKEN = ""  # Set your token here if you don't want to retype it every time.

    parser = argparse.ArgumentParser(description="Fetch emails from GitHub commits by author username.")
    parser.add_argument("-u", "--username", required=True, help="GitHub username to search commits for.")
    parser.add_argument("-t", "--token", required=False, help="GitHub personal access token.")

    args = parser.parse_args()

    username = args.username
    token = args.token or HARDCODED_TOKEN

    if not token:
        token = input("Please enter your GitHub token: ")

    if not token:
        print("Error: GitHub token is required.")
        return

    print(f"Fetching emails for username: {username}")
    emails = get_emails(username, token)

    print("\nFound emails:")
    for email in emails:
        print(email)


if __name__ == "__main__":
    main()

