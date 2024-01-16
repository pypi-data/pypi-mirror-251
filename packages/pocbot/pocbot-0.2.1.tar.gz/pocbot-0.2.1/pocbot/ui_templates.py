"""
Streamlit chatbot UI template
"""
# imports
from typing import List, Any
import streamlit as st
from pocbot.chain_templates import ChatBotChain, SingleModelChatBotChain


class ChatBotUITemplate(object):
    """
    Streamlit chatbot UI template
    - name: name of the chatbot
    - chain: ChatBotChain object.
        The chain object must implement a `invoke` method that takes two arguments:
        - input: input to the chain. This is the query to be processed by the LLM
        - chat_history: Steamlit messages saved to session_sate. It can be converted to a LangChain Memory.
    """
    def __init__(self,
                 name: str,
                 chain: ChatBotChain = None,
                 ):
        self.name = name
        if not isinstance(chain, ChatBotChain):
            raise TypeError("chain must be a ChatBotChain object")
        self.chain = chain
    
    def __call__(self, *args: Any, **kwargs: Any) -> None:
        """Run streamlit app"""

        st.title(f":flying_saucer: {self.name}")

        if "messages" not in st.session_state:
            # a welcome message to the user.
            st.session_state.messages = [{"role": "assistant", "content": f"Welcome to {self.name}! How can I help you?"}]

        # Prompt for user input and save
        if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
                
        # display the existing chat messages
        for message in st.session_state.messages:
            if message["role"] == "system":
                continue
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # If last message is not from assistant, we need to generate a new response
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                resp_container = st.empty()
                with st.spinner("Vasys is Thinking..."):
                    response = self.get_chain_reponse(input=st.session_state.messages[-1]["content"],
                                                      chat_history=st.session_state.messages[1:-1])  # remove system message & last user message
                resp_container.markdown(response)
                message = {"role": "assistant", "content": response}
                st.session_state.messages.append(message)

    def get_chain_reponse(self, input: str, chat_history: List[Any]) -> str:
        """Get response from chain model"""
        if not self.chain:
            return "I'm sorry, I don't have answering abilities. Add an LLM to me!"
        else:
            response = self.chain.invoke(input=input, chat_history=chat_history)
            return response


class SingleModelChatBotUITemplate(object):
    """
    Streamlit chatbot UI template
    - name: name of the chatbot
    - chain: ChatBotChain object.
        The chain object must implement a `invoke` method that takes two arguments:
        - input: input to the chain. This is the query to be processed by the LLM
        - chat_history: Steamlit messages saved to session_sate. It can be converted to a LangChain Memory.
    """
    def __init__(self,
                 name: str,
                 chain: SingleModelChatBotChain = None,
                 ):
        self.name = name
        if not isinstance(chain, SingleModelChatBotChain):
            raise TypeError("chain must be a ChatBotChain object")
        self.chain = chain
    
    def __call__(self, *args: Any, **kwargs: Any) -> None:
        """Run streamlit app"""

        st.title(f":flying_saucer: {self.name}")
        # Sidebar
        st.sidebar.title("Assistant Options")
        model = st.sidebar.selectbox(
            "Model",
            [
                "gpt-3.5-turbo",
                "gpt-4-1106-preview",
                "gpt-4",
            ],
        )
        temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.01)


        if "messages" not in st.session_state:
            # a welcome message to the user.
            st.session_state.messages = [{"role": "assistant", "content": f"Welcome to {self.name}! How can I help you?"}]

        # Prompt for user input and save
        if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
                
        # display the existing chat messages
        for message in st.session_state.messages:
            if message["role"] == "system":
                continue
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # If last message is not from assistant, we need to generate a new response
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                resp_container = st.empty()
                with st.spinner("Vasys is Thinking..."):
                    response = self.get_chain_reponse(input=st.session_state.messages[-1]["content"],
                                                      chat_history=st.session_state.messages[1:-1],  # remove system message & last user message
                                                      model=model,
                                                      temperature=temperature)
                resp_container.markdown(response)
                message = {"role": "assistant", "content": response}
                st.session_state.messages.append(message)

    def get_chain_reponse(self, input: str, chat_history: List[Any], model:str, temperature:float) -> str:
        """Get response from chain model"""
        if not self.chain:
            return "I'm sorry, I don't have answering abilities. Add an LLM to me!"
        else:
            response = self.chain.invoke(input=input, chat_history=chat_history, model=model, temperature=temperature)
            return response
