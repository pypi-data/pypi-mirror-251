"""
Chain interface template
"""
from typing import List, Any
from abc import ABC, abstractmethod


class ChatBotChain(ABC):
    """
    This is the most basic interface for a chatbot chain model. It is the most general one.
    The chain must implement an `invoke` method in order to interact with the chatbot. 
    If not implemented, it will raise an error.
    """

    @abstractmethod
    def invoke(self, input: str, chat_history: List[Any]) -> str:
        """given a question, return an answer.
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
    def invoke(self, input: str, chat_history: List[Any], model: str, temperature: float) -> str:
        """given a question, return an answer.
        - input: input to the chain. This is the query to be processed by the LLM
        - chat_history: Steamlit messages saved to session_sate."""
        raise NotImplementedError("invoke not implemented")

    @abstractmethod
    def _build_chain(self, model: str, temperature: float) -> Any:
        """Build the chain model
        This method will usually be called within the invoke method.
        It should return a LangChain object.
        """
        raise NotImplementedError("_build_chain not implemented")  
