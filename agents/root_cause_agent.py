import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def root_cause_agent(anomaly_report, relevant_evidence):

    prompt = f"""
You are Agent 2 in an Intelligent Log Anomaly Detection
and Root Cause Analysis system.

Your role is ONLY root cause analysis.

You will receive:

1. Anomaly findings from Agent 1
2. Relevant evidence extracted from the log

Analyze ALL detected anomalies.

For each anomaly, determine:

1. The most likely root cause.
2. Why it is considered the root cause.
3. How it produced the observed symptoms.
4. What evidence supports the conclusion.
5. Whether the cause is confirmed or only a possible explanation.

IMPORTANT:

- Multiple root causes may exist.
- Do not assume there is only one root cause.
- Do not invent facts that are not supported by the evidence.
- Clearly distinguish confirmed evidence from possible causes.
- If the exact root cause cannot be determined, state that explicitly.
- Do NOT recommend fixes.
- Do NOT provide code.
- Do NOT provide configuration changes.

IMPORTANT CERTAINTY RULE:

Do not mark a root cause as CONFIRMED merely because
it is a reasonable explanation.

Use CONFIRMED only when the provided evidence directly
establishes the cause.

Use LIKELY when the evidence strongly supports the cause
but does not prove it.

Use POSSIBLE when the cause is plausible but insufficiently
supported.

If the exact root cause cannot be determined from the
available evidence, explicitly state:

"The exact root cause cannot be determined from the
available log evidence."

Do not infer that a specific query, process, server action,
configuration, resource exhaustion, crash, or timeout caused
an anomaly unless the evidence explicitly supports it.

Return ONLY valid JSON in this format:

{{
    "root_causes": [
        {{
            "anomaly": "Related anomaly",
            "root_cause": "Most likely root cause",
            "explanation": "Why this is the likely cause",
            "evidence": [
                "Evidence supporting the conclusion"
            ],
            "certainty": "CONFIRMED | LIKELY | POSSIBLE"
        }}
    ]
}}

Agent 1 Anomaly Findings:
-------------------------
{anomaly_report}

Relevant Log Evidence:
----------------------
{relevant_evidence}
"""

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )

    return response.text