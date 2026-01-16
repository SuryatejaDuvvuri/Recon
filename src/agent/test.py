# test.py
from tools import fetchDiff, postPR
from loop import reviewPR

# Test fetchDiff
pr_number = 2  
diff = fetchDiff(pr_number)
print("Diff:", diff[:200])  # First 200 chars



# Test postPR
test_result = {
    "risk_level": "LOW",
    "summary": "Test comment from Recon",
    "focus_areas": ["test.py"],
    "evidence": ["This is a test"]
}
success = postPR(pr_number, test_result)
print("Posted:", success)