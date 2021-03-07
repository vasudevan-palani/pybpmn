import logging

from datetime import datetime
from .task import Task

logger = logging.getLogger(__name__)

class EndEvent(Task):
    def __init__(self,activity_data,process_instance):
        self.activity_data = activity_data
        self.process_instance = process_instance

    def execute(self,context):

        self._execute(context)

        context[self.activity_data.get("@name","end")] = {
            "start_time" : datetime.now(),
            "end_time" : datetime.now()
        }
        context["status"] = "COMPLETED"
        
        self.process_instance.evaluate_results(self.get_outgoing_activities())