from abc import ABC, abstractmethod

class BaseClient(ABC):
    @abstractmethod
    def create_con(self, params: dict):
        pass

    @abstractmethod
    def pacs_pull(self):
        pass

    @abstractmethod
    def anonymize(self, params: dict):
        pass

    @abstractmethod
    def pacs_push(self):
        pass