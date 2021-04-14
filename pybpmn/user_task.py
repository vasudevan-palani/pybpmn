import logging
from datetime import datetime

from .task import Task

logger = logging.getLogger(__name__)

class UserTask(Task):

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
        
    def complete(self,input_task_context):
        name = self.name
        task = self.task_context
        context = self.context
        payload = self.payload
        payload_task = self.payload_task

        if self.process_instance.handler != None:

            if hasattr(self.process_instance.handler,f"on_exit_{name}"):
                getattr(self.process_instance.handler,f"on_exit_{name}")(context = context,task = payload_task, payload = payload)
            
            if hasattr(self.process_instance.handler,f"on_exit_task"):
                getattr(self.process_instance.handler,f"on_exit_task")(context = context,task = payload_task, payload = payload)

        task["end_time"] = datetime.now()
        task["status"] = "COMPLETED"
        task.update(input_task_context)

        self.process_instance.evaluate_results(self.get_outgoing_activities())