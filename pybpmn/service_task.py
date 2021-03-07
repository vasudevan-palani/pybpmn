import logging
from datetime import datetime
from .task import Task

logger = logging.getLogger(__name__)

class ServiceTask(Task):
    def __init__(self,activity_data,process_instance):
        
        super().__init__(activity_data,process_instance)

        self.activity_data = activity_data
        self.process_instance = process_instance

    def execute(self,context):
        self._execute(context)
        name = self.name
        task = self.task_context
        
        getattr(self.process_instance.handler,f"on_enter_task")(context = context,task = task)
        getattr(self.process_instance.handler,f"on_enter_{name}")(context = context,task = task)
        getattr(self.process_instance.handler,f"on_{name}")(context = context,task = task)
        getattr(self.process_instance.handler,f"on_exit_{name}")(context = context,task = task)
        getattr(self.process_instance.handler,f"on_exit_task")(context = context,task = task)
        context[name]["end_time"] = datetime.now()
        
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