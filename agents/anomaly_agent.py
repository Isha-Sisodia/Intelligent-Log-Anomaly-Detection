import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def anomaly_detection_agent(log_text):

    prompt = f"""
You are Agent 1 in an Intelligent Log Anomaly Detection
and Root Cause Analysis system.

Your role is ONLY anomaly detection.

Analyze the provided application log and identify ALL
significant anomalies.

The system must be general-purpose. Do not assume that
the problem is related to databases, APIs, authentication,
files, or any specific category.

Look for:

- errors
- warnings
- exceptions
- unusual patterns
- repeated failures
- timeouts
- failed requests
- dependency failures
- configuration problems
- authentication/authorization failures
- permission problems
- any other suspicious behavior

IMPORTANT:

1. Identify ALL significant anomalies.
2. Multiple anomalies may exist in the same log.
3. Do not stop after finding the first anomaly.
4. Do not assume a root cause.
5. Do not recommend fixes.
6. Use only evidence present in the log.
7. Preserve the important log lines that support each anomaly.

IMPORTANT ANOMALY GROUPING RULES:

- Group repeated occurrences of the same error or failure
  pattern into a single anomaly.
- Do not create a separate anomaly for every repeated log line.
- If the same error occurs multiple times, keep the occurrences
  as evidence under one anomaly.
- Combine closely related errors that represent the same
  failure pattern.
- Only create separate anomalies when they represent
  meaningfully different problems.

Return ONLY valid JSON in this format:

{{
    "anomalies": [
        {{
            "title": "Short name of anomaly",
            "severity": "LOW | MEDIUM | HIGH | CRITICAL",
            "description": "What happened",
            "evidence": [
                "Relevant log line 1",
                "Relevant log line 2"
            ],
            "pattern": "Relevant error or failure pattern"
        }}
    ],
    "relevant_evidence": [
        "Important log line or context",
        "Another relevant log line"
    ]
}}

If no significant anomaly exists, return:

{{
    "anomalies": [],
    "relevant_evidence": []
}}

LOG:

{log_text}
"""

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )

    return response.text