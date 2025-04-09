import streamlit as st
import openai

st.title("🤖 AI Agents Negotiation")

# Input prompts
agent1_prompt = st.text_area("Buyer System Prompt", "You are a shrewd negotiator representing a tech company.")
agent2_prompt = st.text_area("Seller System Prompt", "You are a diplomatic negotiator representing a government agency.")

# Initialize session state
if "negotiation_active" not in st.session_state:
    st.session_state.negotiation_active = False
if "agent1_messages" not in st.session_state:
    st.session_state.agent1_messages = []
if "agent2_messages" not in st.session_state:
    st.session_state.agent2_messages = []
if "round" not in st.session_state:
    st.session_state.round = 0
if "pending_response" not in st.session_state:
    st.session_state.pending_response = False

# Start negotiation
if st.button("Start Negotiation"):
    st.session_state.negotiation_active = True
    st.session_state.round = 0
    st.session_state.agent1_messages = [
        {"role": "system", "content": agent1_prompt},
        {"role": "user", "content": "Let's begin the negotiation. What’s your proposal?"}
    ]
    st.session_state.agent2_messages = [
        {"role": "system", "content": agent2_prompt}
    ]
    st.session_state.pending_response = True
    st.rerun()

# Stop negotiation
if st.session_state.negotiation_active and st.button("Stop Negotiation"):
    st.session_state.negotiation_active = False
    st.session_state.pending_response = False
    st.success("Negotiation stopped.")

# Display chat so far
if st.session_state.round > 0 or st.session_state.agent1_messages:
    st.subheader("📝 Conversation History")
    for i in range(1, len(st.session_state.agent1_messages)):
        if "content" in st.session_state.agent1_messages[i]:
            st.markdown(f"**Agent 1:** {st.session_state.agent1_messages[i]['content']}")
        if i < len(st.session_state.agent2_messages) and "content" in st.session_state.agent2_messages[i]:
            st.markdown(f"**Agent 2:** {st.session_state.agent2_messages[i]['content']}")

# Run a round if flagged
if (
    st.session_state.negotiation_active
    and st.session_state.pending_response
    and st.session_state.round < 15
):
    with st.spinner(f"Negotiation round {st.session_state.round + 1}..."):

        # Agent 1 responds
        agent1_response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.agent1_messages
        ).choices[0].message.content

        st.session_state.agent1_messages.append({"role": "assistant", "content": agent1_response})
        st.session_state.agent2_messages.append({"role": "user", "content": agent1_response})

        # Agent 2 responds
        agent2_response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.agent2_messages
        ).choices[0].message.content

        st.session_state.agent2_messages.append({"role": "assistant", "content": agent2_response})
        st.session_state.agent1_messages.append({"role": "user", "content": agent2_response})

        # Advance round and prepare next
        st.session_state.round += 1
        st.session_state.pending_response = True if st.session_state.round < 15 else False

    st.rerun()

# Show complete message
if st.session_state.round >= 15 and st.session_state.negotiation_active:
    st.session_state.negotiation_active = False
    st.session_state.pending_response = False
    st.success("✅ Negotiation completed.")
