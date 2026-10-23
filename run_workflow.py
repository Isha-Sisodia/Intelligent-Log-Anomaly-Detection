from workflow import app

# This is manual to write log file name every time. 
# Read the log file
# with open("logs/multiple_errors.log", "r", encoding="utf-8") as file:
#     log_text = file.read()

import sys

log_file = sys.argv[1]

with open(log_file, "r") as f:
    log_text = f.read()

# Initial state
initial_state = {
    "log_text": log_text,
    "anomaly_report": "",
    "relevant_evidence": "",
    "root_cause_report": "",
    "fix_report": ""
}


# Run LangGraph workflow
result = app.invoke(initial_state)


# Display final results

print("\n========== AGENT 1: ANOMALY DETECTION ==========\n")
print(result["anomaly_report"])

print("\n========== AGENT 2: ROOT CAUSE ANALYSIS ==========\n")
print(result["root_cause_report"])

print("\n========== AGENT 3: FIX RECOMMENDATION ==========\n")
print(result["fix_report"])