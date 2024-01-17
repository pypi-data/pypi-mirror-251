from abc import ABC, abstractmethod
class Block(ABC):
    """
    Abstract class representing a block in the report
    This is not meant to be used directly but to be inherited by specific block classes
    """
    @abstractmethod
    def _as_html(self):
        ...
