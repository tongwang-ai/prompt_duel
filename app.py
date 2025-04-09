import streamlit as st
import openai
import time

st.title("🤖 AI Agents Negotiation")

# Input prompts for both agents
agent1_prompt = st.text_area("Agent 1 System Prompt", "You are a shrewd negotiator representing a tech company.")
agent2_prompt = st.text_area("Agent 2 System Prompt", "You are a diplomatic negotiator representing a government agency.")

# Initialize session state
if "negotiation_active" not in st.session_state:
    st.session_state.negotiation_active = False
if "agent1_messages" not in st.session_state:
    st.session_state.agent1_messages = []
if "agent2_messages" not in st.session_state:
    st.session_state.agent2_messages = []
if "round" not in st.session_state:
    st.session_state.round = 0

# Start negotiation
if st.button("Start Negotiation"):
    st.session_state.negotiation_active = True
    st.session_state.round = 0
    st.session_state.agent1_messages = [{"role": "system", "content": agent1_prompt},
                                        {"role": "user", "content": "Let's begin the negotiation. What’s your proposal?"}]
    st.session_state.agent2_messages = [{"role": "system", "content": agent2_prompt}]
    st.rerun()

# Stop negotiation
if st.session_state.negotiation_active and st.button("Stop Negotiation"):
    st.session_state.negotiation_active = False
    st.success("Negotiation stopped.")

# Run the negotiation
if st.session_state.negotiation_active and st.session_state.round < 15:
    with st.spinner(f"Negotiation round {st.session_state.round + 1}..."):

        # Agent 1 replies
        time.sleep(0.5)
        agent1_response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.agent1_messages
        ).choices[0].message.content
        st.markdown(f"**Agent 1:** {agent1_response}")
        st.session_state.agent2_messages.append({"role": "user", "content": agent1_response})

        # Agent 2 replies
        time.sleep(0.5)
        agent2_response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.agent2_messages
        ).choices[0].message.content
        st.markdown(f"**Agent 2:** {agent2_response}")
        st.session_state.agent1_messages.append({"role": "user", "content": agent2_response})

        st.session_state.round += 1

    st.rerun()


elif st.session_state.round >= 15:
    st.session_state.negotiation_active = False
    st.success("Negotiation completed.")
