import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def fix_recommendation_agent(
    anomaly_report,
    relevant_evidence,
    root_cause_report
):

    prompt = f"""
You are Agent 3 in an Intelligent Log Anomaly Detection
and Root Cause Analysis system.

Your role is ONLY fix recommendation.

You will receive:

1. Anomaly findings from Agent 1
2. Relevant evidence from the log
3. Root cause analysis from Agent 2

Provide practical recommendations for ALL identified
root causes.

For each root cause provide:

1. Recommended fix
2. Why the fix is appropriate
3. Implementation steps
4. Configuration changes, if applicable
5. Code changes, if applicable
6. Verification steps

IMPORTANT:

- Multiple problems may exist.
- Provide recommendations for each relevant problem.
- Do NOT automatically modify source code.
- Only recommend changes.
- Do NOT invent facts.
- Do NOT recommend a specific configuration value unless
  the provided evidence directly supports that value.
- Do NOT invent numeric values, thresholds, timeouts,
  connection limits, retry counts, or configuration settings.
- If the root cause is uncertain, recommend diagnostic
  steps before suggesting a specific fix.
- If the exact root cause cannot be determined, prefer
  investigation and verification steps over specific
  configuration or code changes.
- If you mention a configuration setting, describe what
  should be investigated rather than inventing a value.
- The application in this project uses Python and Django.
- If code examples are required, provide Python/Django
  code only.
- Do NOT provide Java, Spring Boot, or other framework code.

UNCERTAINTY RULE:

If Agent 2 marks the root cause as POSSIBLE or LIKELY,
do not present a specific configuration value or code change
as the recommended solution unless Agent 2's evidence directly
supports that specific change.

In uncertain cases, provide:
1. Diagnostic steps
2. What evidence to look for
3. Possible fixes only at a general level
4. Verification steps

Return ONLY valid JSON in this format:

{{
    "recommendations": [
        {{
            "root_cause": "Related root cause",
            "recommended_fix": "Recommended solution",
            "reason": "Why this fix is appropriate",
            "steps": [
                "Step 1",
                "Step 2"
            ],
            "configuration": "Configuration change if applicable",
            "code_change": "Code change if applicable",
            "verification": [
                "Verification step"
            ]
        }}
    ]
}}

Agent 1 Findings:
-----------------
{anomaly_report}

Relevant Evidence:
------------------
{relevant_evidence}

Agent 2 Root Cause Analysis:
----------------------------
{root_cause_report}
"""

    response = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )

    return response.text