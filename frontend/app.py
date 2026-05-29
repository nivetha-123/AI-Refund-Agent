
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import requests


st.set_page_config(
    page_title="AI Refund Agent",
    layout="wide"
)

st.title("AI Customer Support Refund Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "logs" not in st.session_state:
    st.session_state.logs = []


chat_col, admin_col = st.columns([2, 1])

with chat_col:

    st.header("Customer Chat")

    # DISPLAY CHAT HISTORY
    for msg in st.session_state.messages:

        with st.chat_message(msg["role"]):

            if msg["role"] == "assistant":

                decision = msg.get("decision")

                if decision == "APPROVED":
                    st.success(f"✅ DECISION: {decision}")

                elif decision == "DENIED":
                    st.error(f"❌ DECISION: {decision}")

                elif decision == "ESCALATED":
                    st.warning(f"⚠️ DECISION: {decision}")
                

                st.write(msg["content"])

            else:
                st.write(msg["content"])

    # CHAT INPUT
    user_input = st.chat_input(
        "Type your refund request..."
    )

    if user_input:

        # SAVE USER MESSAGE
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        try:

            # SEND REQUEST TO BACKEND
            response = requests.post(
                "http://backend:8000/chat",
                json={
                    "messages": [
                        {
                            "role": "user",
                            "content": user_input
                        }
                    ]
                },
                timeout=120
            )

            # HANDLE BACKEND ERROR
            if response.status_code != 200:

                assistant_response = f"Backend Error: {response.text}"
                decision = "ERROR"
                logs = []

            else:

                data = response.json()

                assistant_response = data.get("response", "")
                decision = data.get("decision", "UNKNOWN")
                logs = data.get("logs", [])

        except Exception as e:

            assistant_response = f"Error: {str(e)}"
            decision = "ERROR"
            logs = []

        # SAVE ASSISTANT MESSAGE
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_response,
            "decision": decision
        })

        # SAVE LOGS
        st.session_state.logs = logs

        st.rerun()


with admin_col:

    st.header("Admin Dashboard")

    st.subheader("Reasoning Logs")

    if not st.session_state.logs:
        st.info("No logs yet")

    for log in st.session_state.logs:
        print(log,'logloglog')
        if log["type"] == "step":

            step = log["step"]

            if step["type"] == "agent_thinking":

                st.info(
                    f"🤖 {step['text']}"
                )

            elif step["type"] == "tool_call":

                st.warning(
                    f"🛠 Tool: {step['tool']}"
                )

                st.code(step["input"])

            elif step["type"] == "policy_validation":

                st.success(
                    f"✅ {step['text']}"
                )
            elif step["type"] == "security_alert":
                st.error(f"🚨 SECURITY ALERT: {step['text']}")

        elif log["type"] == "final":

            decision = log["decision"]

            if decision == "APPROVED":
                st.success(f"🎯 {decision}")

            elif decision == "DENIED":
                st.error(f"🎯 {decision}")

            elif decision == "ESCALATED":
                st.warning(f"🎯 {decision}")

    # CLEAR CHAT BUTTON
    st.divider()

    if st.button("Clear Chat"):

        st.session_state.messages = []
        st.session_state.logs = []

        st.rerun()

