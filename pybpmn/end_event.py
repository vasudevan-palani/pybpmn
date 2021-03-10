import logging

from datetime import datetime
from .task import Task

logger = logging.getLogger(__name__)

class EndEvent(Task):

    def execute(self,context,payload):

        self._execute(context,payload)

        self.task_context["start_time"] = datetime.now()
        self.task_context["end_time"] = datetime.now()

        context["status"] = "COMPLETED"
        
        self.process_instance.evaluate_results(self.get_outgoing_activities())