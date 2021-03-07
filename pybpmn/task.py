import abc
from datetime import datetime
from .component import BpmnComponent
import uuid
import logging

logger = logging.getLogger(__name__)

class Task(BpmnComponent):

    def __init__(self,activity_data,process_instance):
        self.activity_data = activity_data
        self.process_instance = process_instance

    @abc.abstractmethod
    def execute(self,context):
        pass
    
    def _execute(self,context):
        self.context = context
        self.name = self.activity_data.get("@name")
        self.activity_id = str(uuid.uuid4())
        name = self.name
        if ( self.context.get(name) == None ) :
            self.context[name] = {}

        self.task_context = self.context[name]
        self.task_context["start_time"] = datetime.now()
        self.task_context["name"] = name
        self.task_context["activity_id"] = self.activity_id
        
        logger.info({
            "message": f"Executing service task:{name}",
            "data" : self.activity_data
        })