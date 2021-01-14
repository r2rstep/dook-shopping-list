import abc


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def get(self, id):
        pass

    @abc.abstractmethod
    def add(self, obj):
        pass
