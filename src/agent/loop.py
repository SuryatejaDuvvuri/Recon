from ollama import chat, ChatResponse
from src.agent.tools import readFile, searchCodebase
import json
import re

def parseTool(content: str):
    if not content or '"risk_level"' in content:
        return None
    match = re.search(r'"name":\s*"(\w+)".*?(?:"arguments"|"parameters"):\s*(\{[^}]+\})', content, re.DOTALL)
    if match:
        try:
            return {"name": match.group(1), "arguments": json.loads(match.group(2))}
        except:
            return None
    return None


available_functions = {
  'readFile': readFile,
  'searchCodebase': searchCodebase,
}

systemPrompt = """ You are Recon, an agentic code reviewer.

Your job is to assess risk in PR diffs. But you MUST gather context before making judgments.

RULES:
1. NEVER assume what a function does. Use read_file to check
2. ALWAYS search for usages of modified functions
3. ALWAYS check if tests exist for changed code
4. Only give your final assessment after using at least one tool

Available tools:
- readFile(path): Read a file's contents
- searchCodebase(query): Search for patterns in the repo

When you have gathered enough context, respond with ONLY this JSON:
{
    "risk_level": "HIGH" | "MEDIUM" | "LOW",
    "summary": "One sentence explanation",
    "focus_areas": ["files to review"],
    "evidence": ["concrete findings from your investigation"]
}
"""

#Example content
# diffContent = """
# diff --git a/src/auth/login.py b/src/auth/login.py
# index 75cb2d0..67c57d3 100644
# --- a/src/auth/login.py
# +++ b/src/auth/login.py
# @@ -12,7 +12,7 @@ def validate_user(username, password):
#      user = get_user(username)
#      if user and check_password(password, user.password_hash):
# -        return create_session(user)
# +        return create_session(user, remember=True)
#      return None
# """

def reviewPR(diffContent:str) -> dict:
    messages = [{'role': 'system', 'content': systemPrompt}, {'role': 'user', 'content': f"Review this PR diff:\n\n{diffContent}"}]
    while True:
        response: ChatResponse = chat(
            model='qwen2.5-coder:latest',
            messages=messages,
            tools=[readFile, searchCodebase],
            think=False,
        )
        messages.append(response.message)
        print("Content: ", response.message.content)
        if response.message.tool_calls:
            for tc in response.message.tool_calls:
                if tc.function.name in available_functions:
                    print(f"Calling {tc.function.name} with arguments {tc.function.arguments}")
                    result = available_functions[tc.function.name](**tc.function.arguments)
                    print(f"Result: {result}")
                    # add the tool result to the messages
                    messages.append({'role': 'tool', 'tool_name': tc.function.name, 'content': str(result)})
            continue
        parsed = parseTool(response.message.content)
        if parsed and parsed["name"] in available_functions:
            print(f"Calling {parsed['name']} with {parsed['arguments']}")
            result = available_functions[parsed["name"]](**parsed["arguments"])
            messages.append({'role': 'tool', 'tool_name': parsed["name"], 'content': str(result)})
            continue
        
        if '"risk_level"' in (response.message.content or ''):
            print("\nFinal Result")
            print(response.message.content)
            match = re.search(r'\{[^{}]*"risk_level"[^{}]*\}', response.message.content, re.DOTALL)
            if match:
                return json.loads(match.group())
        break

    return {
        "risk_level": "UNKNOWN",
        "summary": "Review could not complete",
        "focus_areas": [],
        "evidence": []
    }
    # continue the loop with the updated messages


