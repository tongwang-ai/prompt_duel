import streamlit as st
import openai

st.title("🤖 AI Agents Negotiation")
# Configure OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Input prompts for both agents
agent1_prompt = st.text_area("Agent 1 System Prompt", "You are a shrewd negotiator representing a tech company.")
agent2_prompt = st.text_area("Agent 2 System Prompt", "You are a diplomatic negotiator representing a government agency.")

# Button to start negotiation
if st.button("Start Negotiation"):
    with st.spinner("Negotiation in progress..."):

        # Setup agents with their system messages
        agent1_messages = [{"role": "system", "content": agent1_prompt}]
        agent2_messages = [{"role": "system", "content": agent2_prompt}]

        # Initial user message to start the conversation
        initial_message = "Let's begin the negotiation. What’s your proposal?"
        agent1_messages.append({"role": "user", "content": initial_message})

        st.markdown("### 🤝 Conversation")

        for round_num in range(15):
            # Agent 1 replies
            agent1_response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=agent1_messages
            ).choices[0].message.content

            agent2_messages.append({"role": "user", "content": agent1_response})
            st.markdown(f"**Agent 1:** {agent1_response}")

            # Agent 2 replies
            agent2_response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=agent2_messages
            ).choices[0].message.content

            agent1_messages.append({"role": "user", "content": agent2_response})
            st.markdown(f"**Agent 2:** {agent2_response}")
