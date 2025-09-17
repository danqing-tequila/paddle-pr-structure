import requests
import time

GITHUB_TOKEN = 'GITHUB'  # Generate from https://github.com/settings/tokens (with repo:public_repo scope)
REPO = 'PaddlePaddle/Paddle'
LABEL = 'Intel'

# Categories with sub-categories and keywords for MECE principle
CATEGORIES = {
    'Operator Optimization': {
        'Fusion': ['fuse'],
        'Speed/Performance': ['speed', 'performance'],
        'Operator': ['op', 'operator']
    },
    'Quantization': {
        'PTQ': ['ptq'],
        'QAT': ['qat'],
        'General Quant': ['int8', 'quant']
    },
    'BF16/Low Precision': {
        'BF16': ['bf16', 'bfloat16'],
        'Low Precision General': ['low precision']
    },
    'CI/Infrastructure': {
        'CI': ['ci', 'continuous integration'],
        'Docker': ['docker'],
        'Workflow': ['workflow']
    },
    'Documentation': {
        'Docs': ['docs', 'doc'],
        'README': ['readme']
    },
    'Bugfix': {
        'Bug': ['bug'],
        'Fix': ['fix'],
        'Issue': ['issue'],
        'Segfault': ['segfault']
    },
    'API/Interface': {
        'API': ['api'],
        'Interface': ['interface']
    },
    'Refactor': {
        'Refactor': ['refactor']
    },
    'Tests': {
        'Test Types': ['test', 'unit test', 'ut']
    },
    'Build': {
        'Build/Compile': ['build', 'cmake', 'compile']
    }
}

PER_PAGE = 100  # GitHub API max is 100

# --------- Helper Functions ---------

def categorize_pr_mece(title, body):
    combined = (title + ' ' + (body or '')).lower()
    for cat in sorted(CATEGORIES):
        subcats = CATEGORIES[cat]
        for subcat in sorted(subcats):
            keywords = subcats[subcat]
            for kw in keywords:
                if kw in combined:
                    return cat, subcat
    return None, None

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
        link = resp.headers.get('Link', '')
        next_url = None
        if link:
            parts = link.split(',')
            for part in parts:
                if 'rel="next"' in part:
                    next_url = part[part.find('<') + 1:part.find('>')]
                    break
        url = next_url
        time.sleep(0.5)
    return prs

def main():
    prs = get_all_intel_prs()
    # Create nested dictionary for categories and sub-categories result storage
    categories = {cat: {subcat: [] for subcat in subcats} for cat, subcats in CATEGORIES.items()}
    uncategorized = []
    for pr in prs:
        title = pr.get('title', '')
        body = pr.get('body', '')
        url = pr.get('html_url', '')
        pr_number = pr.get('number')
        category, subcategory = categorize_pr_mece(title, body)
        entry = {"number": pr_number, "title": title, "url": url}
        if category and subcategory:
            categories[category][subcategory].append(entry)
        else:
            uncategorized.append(entry)

    # Output categorized PRs with sub-categories
    for cat, subcats in categories.items():
        total_cat = sum(len(items) for items in subcats.values())
        print(f'\n### {cat} ({total_cat})')
        for subcat, items in subcats.items():
            if items:
                print(f'#### {subcat} ({len(items)})')
                for entry in items:
                    print(f"- [#{entry['number']}]({entry['url']}): {entry['title']}")
    
    print(f'\n### Uncategorized PRs ({len(uncategorized)})')
    for entry in uncategorized:
        print(f"- [#{entry['number']}]({entry['url']}): {entry['title']}")

if __name__ == '__main__':
    main()
