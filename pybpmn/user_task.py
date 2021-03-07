import logging
from datetime import datetime

from .task import Task

logger = logging.getLogger(__name__)

class UserTask(Task):

    def execute(self,context):
        
        self._execute(context)

        name = self.name

        task = self.task_context
        task["status"] = "STARTED"

        getattr(self.process_instance.handler,f"on_enter_task")(context = context,task = task)
        getattr(self.process_instance.handler,f"on_enter_{name}")(context = context,task = task)
        
    def complete(self,input_task_context):
        name = self.name
        task = self.task_context
        context = self.context

        self.process_instance.evaluate_results(self.get_outgoing_activities())
        getattr(self.process_instance.handler,f"on_exit_{name}")(context = context,task = task)
        getattr(self.process_instance.handler,f"on_exit_task")(context = context,task = task)
        task["end_time"] = datetime.now()
        task["status"] = "COMPLETED"
        task.update(input_task_context)

        self.process_instance.evaluate_results(self.get_outgoing_activities())