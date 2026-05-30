# controllers/base_controller.py

from abc import ABC, abstractmethod

class ICTControllerBase(ABC):
    @abstractmethod
    def connect(self):
        ...

    @abstractmethod
    def load_testplan(self, path: str):
        ...

    @abstractmethod
    def list_tests(self):
        ...

    @abstractmethod
    def run_test(self, test_name: str):
        ...

    @abstractmethod
    def fixture_close(self):
        ...

    @abstractmethod
    def fixture_open(self):
        ...

    @abstractmethod
    def disconnect(self):
        ...
