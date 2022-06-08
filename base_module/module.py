import logging
from abc import ABC, abstractmethod


class Module(ABC):

    @abstractmethod
    def __init__(self, module_name, log_level):
        logging.basicConfig(level=log_level)
        self._logger = logging.getLogger(module_name)