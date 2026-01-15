import base64
import requests
import os

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

def readFile(path: str) -> str:
    url = f'https://api.github.com/repos/SuryatejaDuvvuri/Recon/contents/{path}'
    headers = {'Authorization': f'Bearer {GITHUB_TOKEN}'}
    
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        content = base64.b64decode(req.json()['content']).decode('utf-8')
        return content
    else:
        return "Content not found"
    
def searchCodebase(query: str) -> str:
    url = f'https://api.github.com/search/code?q={query}+repo:SuryatejaDuvvuri/Recon'
    headers = {
        'Authorization': f'Bearer {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        items = req.json().get('items', [])
        results = [f"{item['path']}: {item['name']}" for item in items[:5]]
        return "\n".join(results) if results else "No matches found"
    else:
        return f"Search failed: {req.status_code}"