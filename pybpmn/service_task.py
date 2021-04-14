import logging
from datetime import datetime
from .task import Task

logger = logging.getLogger(__name__)

class ServiceTask(Task):
    def __init__(self,activity_data,process_instance):
        
        super().__init__(activity_data,process_instance)

        self.activity_data = activity_data
        self.process_instance = process_instance

    def execute(self,context,payload):
        self._execute(context,payload)
        name = self.name
        task = self.task_context
        task["status"] = "STARTED"
        payload_task = self.payload_task

        if self.process_instance.handler != None:
            if hasattr(self.process_instance.handler,f"on_enter_task"):
                getattr(self.process_instance.handler,f"on_enter_task")(context = context,task = payload_task, payload = payload)
                
            if hasattr(self.process_instance.handler,f"on_enter_{name}"):
                getattr(self.process_instance.handler,f"on_enter_{name}")(context = context,task = payload_task, payload = payload)
            
            if hasattr(self.process_instance.handler,f"on_{name}"):
                getattr(self.process_instance.handler,f"on_{name}")(context = context,task = payload_task, payload = payload)

            if hasattr(self.process_instance.handler,f"on_exit_{name}"):
                getattr(self.process_instance.handler,f"on_exit_{name}")(context = context,task = payload_task, payload = payload)

            if hasattr(self.process_instance.handler,f"on_exit_task"):
                getattr(self.process_instance.handler,f"on_exit_task")(context = context,task = payload_task, payload = payload)
        
        context[name]["end_time"] = datetime.now()
        task["status"] = "COMPLETED"
        
        self.process_instance.evaluate_results(self.get_outgoing_activities())