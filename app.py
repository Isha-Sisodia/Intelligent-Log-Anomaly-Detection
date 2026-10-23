import streamlit as st
import json

from workflow import app


# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="Intelligent Log Analyzer",
    page_icon="🔍",
    layout="wide"
)


# -------------------------
# Header
# -------------------------

st.title("🔍 Intelligent Log Analyzer")

st.write(
    "Upload an application log file to detect anomalies, "
    "identify possible root causes, and receive fix recommendations."
)


# -------------------------
# File Upload
# -------------------------

uploaded_file = st.file_uploader(
    "Upload your .log file",
    type=["log"]
)


# -------------------------
# Analyze Button
# -------------------------

if uploaded_file is not None:

    st.success(f"File uploaded: {uploaded_file.name}")

    if st.button("🔎 Analyze Log"):

        log_text = uploaded_file.read().decode("utf-8")

        initial_state = {
            "log_text": log_text,
            "anomaly_report": "",
            "relevant_evidence": "",
            "root_cause_report": "",
            "fix_report": ""
        }

        with st.spinner("Analyzing log..."):

            result = app.invoke(initial_state)

        # -------------------------
        # Parse Agent 1
        # -------------------------

        anomaly_data = json.loads(
            result["anomaly_report"]
        )

        anomalies = anomaly_data.get("anomalies", [])

        # -------------------------
        # No Anomalies
        # -------------------------

        if not anomalies:

            st.success("✅ No significant anomalies detected.")

            st.info(
                "The provided log indicates normal system operation."
            )

        # -------------------------
        # Anomalies Found
        # -------------------------

        else:

            st.header("📊 Analysis Result")

            for anomaly in anomalies:

                st.subheader(
                    f"⚠️ {anomaly['title']}"
                )

                st.write(
                    f"**Severity:** {anomaly['severity']}"
                )

                st.write(
                    f"**Description:** {anomaly['description']}"
                )

                with st.expander("View Evidence"):

                    for evidence in anomaly["evidence"]:
                        st.write(f"- {evidence}")

                st.write(
                    f"**Pattern:** {anomaly['pattern']}"
                )

            # -------------------------
            # Agent 2
            # -------------------------

            st.divider()

            with st.expander(
                "🤖 View Agent 2 — Root Cause Analysis"
            ):

                root_cause_data = json.loads(
                    result["root_cause_report"]
                )

                for root_cause in root_cause_data[
                    "root_causes"
                ]:

                    st.subheader(
                        root_cause["anomaly"]
                    )

                    st.write(
                        f"**Root Cause:** "
                        f"{root_cause['root_cause']}"
                    )

                    st.write(
                        f"**Certainty:** "
                        f"{root_cause['certainty']}"
                    )

                    st.write(
                        f"**Explanation:** "
                        f"{root_cause['explanation']}"
                    )

                    with st.expander(
                        "Root Cause Evidence"
                    ):

                        for evidence in root_cause[
                            "evidence"
                        ]:
                            st.write(f"- {evidence}")

            # -------------------------
            # Agent 3
            # -------------------------

            with st.expander(
                "🛠️ View Agent 3 — Fix Recommendation"
            ):

                fix_data = json.loads(
                    result["fix_report"]
                )

                for recommendation in fix_data[
                    "recommendations"
                ]:

                    st.subheader(
                        recommendation["root_cause"]
                    )

                    st.write(
                        f"**Recommended Fix:** "
                        f"{recommendation['recommended_fix']}"
                    )

                    st.write(
                        f"**Reason:** "
                        f"{recommendation['reason']}"
                    )

                    st.write("**Steps:**")

                    for step in recommendation["steps"]:
                        st.write(f"- {step}")

                    st.write(
                        f"**Configuration:** "
                        f"{recommendation['configuration']}"
                    )

                    st.write(
                        f"**Code Change:** "
                        f"{recommendation['code_change']}"
                    )

                    st.write("**Verification:**")

                    for verification in recommendation[
                        "verification"
                    ]:
                        st.write(f"- {verification}")