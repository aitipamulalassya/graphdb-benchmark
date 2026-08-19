from abc import ABC, abstractmethod


class BenchmarkAdapter(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def verify(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def create_schema(self):
        pass

    @abstractmethod
    def load_nodes(self, rows, batch_size):
        pass

    @abstractmethod
    def load_relationships(self, rows, batch_size):
        pass

    @abstractmethod
    def run(self, operation, params):
        pass

    @abstractmethod
    def resource_info(self):
        pass