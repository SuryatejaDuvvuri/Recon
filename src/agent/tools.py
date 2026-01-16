import base64
import requests
import os
from dotenv import load_dotenv

load_dotenv()

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
def getDiff(url:str) -> str:
    # url = f'https://api.github.com/repos/SuryatejaDuvvuri/Recon/pulls/{prNum}'
    headers = {'Authorization': f'Bearer {GITHUB_TOKEN}','Accept':"application/vnd.github.diff" }
    
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        return req.text
    else:
        return "Content not found"
    
def postPR(prNum:int, result) -> bool:
    url = f'https://api.github.com/repos/SuryatejaDuvvuri/Recon/issues/{prNum}/comments'
    headers = {'Authorization': f'Bearer {GITHUB_TOKEN}'}
    comment = f"""## Recon Assessment
    **Risk Level:** {result.get('risk_level', 'UNKNOWN')}

    **Summary:** {result.get('summary', 'No summary')}

    **Focus Areas:** {', '.join(result.get('focus_areas', []))}

    **Evidence:**
    {chr(10).join('- ' + e for e in result.get('evidence', []))}
    """
    
    req = requests.post(url, headers=headers,json={"body": comment})
    if req.status_code == 201:
        return True
    else:
        return False
def searchCodebase(query: str = None, path: str = None) -> str:
    
    search = query or path
    if not search:
        return "No proper term provided"
    url = f'https://api.github.com/search/code?q={search}+repo:SuryatejaDuvvuri/Recon'
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