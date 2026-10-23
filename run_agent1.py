from agents.anomaly_agent import anomaly_detection_agent


# Read the log file
with open("logs/sample.log", "r", encoding="utf-8") as file:
    log_text = file.read()


# Send the log content to Agent 1
result = anomaly_detection_agent(log_text)


# Display Agent 1's result
print("\n========== AGENT 1: ANOMALY DETECTION ==========\n")
print(result)