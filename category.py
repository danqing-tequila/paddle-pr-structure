import requests
import time

# --------- Configuration ---------
# categorize each PR based on its title and body content using keyword matching. 
# Non-categorized PRs are listed separately. 
# This script handles paging, does not miss any PR, and can be extended or customized to suit additional needs.

GITHUB_TOKEN = 'GITHUB_TOKEN'  # Generate from https://github.com/settings/tokens (with repo:public_repo scope)
REPO = 'PaddlePaddle/Paddle'
LABEL = 'Intel'
CATEGORIES = {
    'Operator Optimization': ['op', 'operator', 'speed', 'performance', 'fuse'],
    'Quantization': ['int8', 'quant', 'ptq', 'qat'],
    'BF16/Low Precision': ['bf16', 'bfloat16', 'low precision'],
    'CI/Infrastructure': ['ci', 'continuous integration', 'docker', 'workflow'],
    'Documentation': ['docs', 'readme', 'doc'],
    'Bugfix': ['fix', 'bug', 'issue', 'segfault'],
    'API/Interface': ['api', 'interface'],
    'Refactor': ['refactor'],
    'Tests': ['test', 'unit test', 'ut'],
    'Build': ['build', 'cmake', 'compile']
}
PER_PAGE = 100  # GitHub API max is 100

# --------- Helper Functions ---------
def categorize_pr(title, body):
    combined = (title + ' ' + (body or '')).lower()
    for cat, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in combined:
                return cat
    return None

def get_all_intel_prs():
    prs = []
    url = (f'https://api.github.com/search/issues?q=repo:{REPO}+is:pr+is:closed+label:{LABEL}'
           f'&per_page={PER_PAGE}')
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}

    while url:
        print(f"Fetching URL: {url}")
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            print(f"Failed to fetch: {resp.status_code} {resp.text}")
            break
        data = resp.json()
        items = data.get('items', [])
        if not items:
            print("No more items found, breaking loop.")
            break
        prs.extend(items)
        print(f"Fetched {len(prs)} PRs so far")

        # Parse Link header to check if there's a next page URL
        link = resp.headers.get('Link', '')
        next_url = None
        if link:
            parts = link.split(',')
            for part in parts:
                if 'rel="next"' in part:
                    next_url = part[part.find('<') + 1:part.find('>')]
                    break
        url = next_url

        time.sleep(0.5)  # Rate limit delay, otherwise You have exceeded a secondary rate limit. Please wait a few minutes before you try again

    return prs

def main():
    prs = get_all_intel_prs()
    categories = {k: [] for k in CATEGORIES}
    uncategorized = []

    for pr in prs:
        title = pr.get('title', '')
        body = pr.get('body', '')
        url = pr.get('html_url', '')
        pr_number = pr.get('number')
        category = categorize_pr(title, body)
        entry = {"number": pr_number, "title": title, "url": url}
        if category:
            categories[category].append(entry)
        else:
            uncategorized.append(entry)

    # Output categorized PRs
    for cat, items in categories.items():
        print(f'\n### {cat} ({len(items)})')
        for entry in items:
            print(f"- [#{entry['number']}]({entry['url']}): {entry['title']}")
    
    print(f'\n### Uncategorized PRs ({len(uncategorized)})')
    for entry in uncategorized:
        print(f"- [#{entry['number']}]({entry['url']}): {entry['title']}")

if __name__ == '__main__':
    main()
