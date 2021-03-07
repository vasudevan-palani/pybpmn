import abc
class BpmnComponent:
    
    @abc.abstractmethod
    def execute(*args,**kargs):
        pass