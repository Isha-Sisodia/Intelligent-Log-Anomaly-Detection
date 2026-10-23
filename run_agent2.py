from agents.anomaly_agent import anomaly_detection_agent
from agents.root_cause_agent import root_cause_agent


# Read the log file
with open("logs/sample.log", "r", encoding="utf-8") as file:
    log_text = file.read()


# Agent 1: Detect anomalies
anomaly_report = anomaly_detection_agent(log_text)


# Agent 2: Analyze root cause
root_cause_report = root_cause_agent(
    log_text,
    anomaly_report
)


# Display results
print("\n========== AGENT 1: ANOMALY DETECTION ==========\n")
print(anomaly_report)

print("\n========== AGENT 2: ROOT CAUSE ANALYSIS ==========\n")
print(root_cause_report)