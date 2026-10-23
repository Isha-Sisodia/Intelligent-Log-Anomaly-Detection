import json

from agents.anomaly_agent import anomaly_detection_agent
from agents.root_cause_agent import root_cause_agent
from agents.fix_recommendation_agent import fix_recommendation_agent


with open("logs/sample.log", "r", encoding="utf-8") as file:
    log_text = file.read()


# Agent 1
anomaly_report = anomaly_detection_agent(log_text)

anomaly_data = json.loads(anomaly_report)

relevant_evidence = json.dumps(
    anomaly_data.get("relevant_evidence", [])
)


# Agent 2
root_cause_report = root_cause_agent(
    anomaly_report,
    relevant_evidence
)


# Agent 3
fix_report = fix_recommendation_agent(
    anomaly_report,
    relevant_evidence,
    root_cause_report
)


print("\n========== AGENT 1: ANOMALY DETECTION ==========\n")
print(anomaly_report)

print("\n========== AGENT 2: ROOT CAUSE ANALYSIS ==========\n")
print(root_cause_report)

print("\n========== AGENT 3: FIX RECOMMENDATION ==========\n")
print(fix_report)