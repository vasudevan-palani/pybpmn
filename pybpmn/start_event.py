import logging

from datetime import datetime
from .task import Task

logger = logging.getLogger(__name__)

class StartEvent(Task):
    def __init__(self,activity_data,process_instance):
        self.activity_data = activity_data
        self.process_instance = process_instance

    def execute(self,context):

        self._execute(context)

        context[self.activity_data.get("@name","start")] = {
            "start_time" : datetime.now()
        }
        
        self.process_instance.evaluate_results(self.get_outgoing_activities())

    def get_outgoing_activities(self):
        
        outgoingflowid = self.activity_data.get("bpmn:outgoing")

        target_activity_id = None
        target_activity_type = None
        target_activity_data = None
        for seq_flow in self.process_instance.process_definition.get("bpmn:sequenceFlow"):
            if(seq_flow.get("@id") == outgoingflowid):
                 target_activity_id = seq_flow.get("@targetRef")

        for component_name in self.process_instance.process_definition:
            if type(self.process_instance.process_definition[component_name]) == type(dict()):
                component = self.process_instance.process_definition[component_name]
                if component.get("@id") == target_activity_id:
                    target_activity_data = component
                    target_activity_type = component_name

        return [(target_activity_type,target_activity_id,target_activity_data)]
        