from abc import ABC, abstractmethod

class LLMResponsePort(ABC):
    @abstractmethod
    def getLlmResponse(self, conversationPile, question, textsToEmbed, etimToEmbed):
        pass
