import streamlit as st
import openai

import re

def escape_markdown(text):
    return re.sub(r'_', r'\\_', text)



st.title("🤖 AI Agents Negotiation")

# Fixed Buyer Agent System Prompt
buyer_prompt = """Role play as a buyer agent for company Opendoor and chat with me. Your job is to purchase real estate from potential sellers with a price as low as possible. 

    Now negotiate with the home owner of this house which is valued at \$650,000.
    
But your priority is to get the deal done and the second priority is the price.  Output less than 100 words each time."""

# User inputs Seller Agent System Prompt
seller_prompt = st.text_area("Seller System Prompt", "You are trying to sell your home to an agent")

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
        {"role": "system", "content": buyer_prompt},
        {"role": "user", "content": "Let's begin the negotiation. What’s your proposal?"}
    ]
    st.session_state.agent2_messages = [
        {"role": "system", "content": seller_prompt}
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
    
    for i, msg in enumerate(st.session_state.agent1_messages):
        if msg["role"] == "system":
            continue
        if msg["role"] == "user":
            speaker = "Seller"
        elif msg["role"] == "assistant":
            speaker = "Buyer"
        else:
            speaker = "Unknown"
        #st.write(f"{speaker}: {msg['content']}")
        st.markdown(f"**{speaker}:** {escape_markdown(msg['content'])}")

# Run a round if flagged
if (
    st.session_state.negotiation_active
    and st.session_state.pending_response
    and st.session_state.round < 15
):
    with st.spinner(f"Negotiation round {st.session_state.round + 1}..."):

        # Agent 1 (Buyer) responds
        agent1_response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.agent1_messages
        ).choices[0].message.content

        st.session_state.agent1_messages.append({"role": "assistant", "content": agent1_response})
        st.session_state.agent2_messages.append({"role": "user", "content": agent1_response})

        # Agent 2 (Seller) responds
        agent2_response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.agent2_messages
        ).choices[0].message.content

        st.session_state.agent2_messages.append({"role": "assistant", "content": agent2_response})
        st.session_state.agent1_messages.append({"role": "user", "content": agent2_response})

        # Agreement check after both replies
        agreement_check_prompt = {
            "role": "system",
            "content": (
                "You are an impartial judge observing a negotiation between two agents (a buyer and a seller). "
                "Determine if an agreement has been reached on the price of the house. "
                "Respond with only one word: 'Yes' if there's a clear agreement, or 'No' if not."
            )
        }

        check_response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[agreement_check_prompt] + st.session_state.agent1_messages[-10:]
        ).choices[0].message.content.strip().lower()

        if "yes" in check_response:
            st.session_state.negotiation_active = False
            st.session_state.pending_response = False
            st.success("✅ Agreement reached. Negotiation completed.")
        else:
            st.session_state.round += 1
            st.session_state.pending_response = True if st.session_state.round < 15 else False

    st.rerun()

# Show final message if rounds exhausted
if st.session_state.round >= 15 and st.session_state.negotiation_active:
    st.session_state.negotiation_active = False
    st.session_state.pending_response = False
    st.success("⚖️ Maximum rounds reached. Negotiation completed.")
