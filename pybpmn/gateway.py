import abc
from .task import Task

class Gateway(Task):
    
    @abc.abstractmethod
    def execute(self,context):
        pass