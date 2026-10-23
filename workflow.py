from typing import TypedDict
import json

from langgraph.graph import StateGraph, START, END

from agents.anomaly_agent import anomaly_detection_agent
from agents.root_cause_agent import root_cause_agent
from agents.fix_recommendation_agent import fix_recommendation_agent


# Shared state between all agents
class LogAnalysisState(TypedDict):
    log_text: str
    anomaly_report: str
    relevant_evidence: str
    root_cause_report: str
    fix_report: str


# -------------------------
# Agent 1 Node
# -------------------------

# Helper funvtion to run Agent 1
def clean_json_response(response):
    response = response.strip()

    if response.startswith("```json"):
        response = response[7:]

    if response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    return response.strip()


def run_anomaly_agent(state: LogAnalysisState):

    anomaly_report = anomaly_detection_agent(
        state["log_text"]
    )
    
    print("RAW AGENT 1 RESPONSE:")
    print(repr(anomaly_report))

    # Extract relevant evidence from Agent 1 JSON
    
    anomaly_report = clean_json_response(anomaly_report)
    
    anomaly_data = json.loads(anomaly_report)

    relevant_evidence = json.dumps(
        anomaly_data.get("relevant_evidence", [])
    )

    return {
        "anomaly_report": anomaly_report,
        "relevant_evidence": relevant_evidence
    }

# -------------------------
# Check whether anomalies exist
# -------------------------

def check_anomalies(state: LogAnalysisState):

    anomaly_data = json.loads(state["anomaly_report"])

    if anomaly_data.get("anomalies"):
        return "has_anomalies"

    return "no_anomalies"

# -------------------------
# Agent 2 Node
# -------------------------

def run_root_cause_agent(state: LogAnalysisState):

    root_cause_report = root_cause_agent(
        state["anomaly_report"],
        state["relevant_evidence"]
    )

    root_cause_report = clean_json_response(root_cause_report)

    return {
        "root_cause_report": root_cause_report
    }


# -------------------------
# Agent 3 Node
# -------------------------

def run_fix_agent(state: LogAnalysisState):

    fix_report = fix_recommendation_agent(
        state["anomaly_report"],
        state["relevant_evidence"],
        state["root_cause_report"]
    )

    fix_report = clean_json_response(fix_report)

    return {
        "fix_report": fix_report
    }


# -------------------------
# Create LangGraph
# -------------------------

graph = StateGraph(LogAnalysisState)


# Add agents as nodes
graph.add_node("anomaly_detection", run_anomaly_agent)
graph.add_node("root_cause_analysis", run_root_cause_agent)
graph.add_node("fix_recommendation", run_fix_agent)


# Define workflow
graph.add_edge(START, "anomaly_detection")

graph.add_conditional_edges(
    "anomaly_detection",
    check_anomalies,
    {
        "has_anomalies": "root_cause_analysis",
        "no_anomalies": END
    }
)

graph.add_edge(
    "root_cause_analysis",
    "fix_recommendation"
)

graph.add_edge(
    "fix_recommendation",
    END
)


# Compile graph
app = graph.compile()