import logging

from datetime import datetime
from .task import Task

logger = logging.getLogger(__name__)

class StartEvent(Task):

    def execute(self,context):

        self._execute(context)

        context["status"] = "STARTED"

        context[self.activity_data.get("@name","start")] = {
            "start_time" : datetime.now(),
            "end_time" : datetime.now()
        }
        
        self.process_instance.evaluate_results(self.get_outgoing_activities())