from abc import ABC, abstractmethod


class Repository(ABC):

    @abstractmethod
    def getAll(self, skip: int = 0, limit: int = 100):
        pass

    @abstractmethod
    def get(self, id: int):
        pass

    @abstractmethod
    def save(self, model):
        pass

    @abstractmethod
    def update(self, model, schema):
        pass

    @abstractmethod
    def delete(self, local_content):
        pass   