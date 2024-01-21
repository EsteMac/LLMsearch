import os
from langchain.llms import OpenAI
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler

# Importing Streamlit - an open-source library for creating custom web apps for machine learning and data science.
import streamlit as st

os.environ["BING_SUBSCRIPTION_KEY"] = "25676c9ecc8048388ac8d5b50651ce35"
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"

# Setting up Streamlit page configuration.
st.set_page_config(page_title="Lanchain Agests + MRKL") # Setting the title of the webpage.
st.title("Lanchain Agents + MRKL") # Displaying a title on the webpage.

# Initializing the 'messages' list in the session state if it doesn't exist. 
# This list keeps track of the conversation in the session.
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you?"} # Default starting message of the chat.
    ]

# Displaying the chat history on the webpage by iterating over each message in the 'messages' list.
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"]) # Each message is displayed according to its 'role'.

# Creating an instance of the 'OpenAI' class with specific parameters. 
llm = OpenAI(temperature=0, streaming=True, openai_api_key="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")

# Loading specific tools with the necessary API keys/credentials
tools = load_tools(
    ["bing-search"], 
    bing_api_key=os.environ["BING_SUBSCRIPTION_KEY"], 
    bing_search_url=os.environ["BING_SEARCH_URL"]
)

# Initializing an agent with the loaded tools, the language model, and specific configurations.
# This 'agent' might be the entity processing user inputs and deciding on responses.
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, # The type of agent being initialized.
    verbose=True # Enables detailed logging.
)

# Waiting for the user to input a message.
if prompt := st.chat_input():
    # Once received, the message is added to the 'messages' list and displayed in the chat interface.
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt) # The user's message is displayed in the chat.

    with st.chat_message("assistant"):
        # Creating a Streamlit callback handler, which might be used for real-time updates in the UI.
        st_callback = StreamlitCallbackHandler(st.container())

        # The agent generates a response based on the conversation history.
        response = agent.run(st.session_state.messages, callbacks=[st_callback])

        # The agent's response is displayed in the chat.
        st.write(response)