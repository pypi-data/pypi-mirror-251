"""
Chain interface template
"""
from typing import Any, Dict
from abc import ABC, abstractmethod


class ChatBotChain(ABC):
    """
    This is the most basic interface for a chatbot chain model. It is the most general one.
    The chain must implement an `invoke` method in order to interact with the chatbot. 
    If not implemented, it will raise an error.
    """

    @abstractmethod
    def invoke(self, input_dict: Dict[str, Any]) -> str:
        """given a question, return an answer.
        To match LangChain's invoke method interface, inputs are passed as a dictionary.
        However, expect the dictionary to contain the following keys:
        - input: input to the chain. This is the query to be processed by the LLM
        - chat_history: Steamlit messages saved to session_sate."""
        raise NotImplementedError("invoke not implemented")


class SingleModelChatBotChain(ABC):
    """
    This is the interface for a chatbot chain model
    The chain must implement an `invoke` method in order to interact with the chatbot. 
    If not implemented, it will raise an error.
    """

    @abstractmethod
    def invoke(self, input_dict: Dict[str, Any]) -> str:
        """given a question, return an answer.
        To match LangChain's invoke method interface, inputs are passed as a dictionary.
        However, expect the dictionary to contain the following keys:
        - input: input to the chain. This is the query to be processed by the LLM
        - chat_history: Steamlit messages saved to session_sate.
        - model: model name to use for inference
        - temperature: temperature to use for inference """
        
        raise NotImplementedError("invoke not implemented")

