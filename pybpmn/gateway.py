import abc
from .task import Task

class Gateway(Task):
    
    @abc.abstractmethod
    def execute(self,context,payload):
        pass