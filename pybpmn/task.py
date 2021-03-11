import abc
from datetime import datetime
from .component import BpmnComponent
import uuid
import logging

logger = logging.getLogger(__name__)

class Task(BpmnComponent):

    def __init__(self,activity_data,process_instance):
        self.id = activity_data.get("@id")
        self.activity_data = activity_data
        self.process_instance = process_instance
        self.name = self.activity_data.get("@name")
        self.activity_id = str(uuid.uuid4())

    @abc.abstractmethod
    def execute(self,context,payload):
        pass
    
    def _execute(self,context,payload):
        self.context = context
        self.payload = payload
        name = self.name
        if ( self.context.get(name) == None ) :
            self.context[name] = {}

        if ( self.payload.get(name) == None ) :
            self.payload[name] = {}

        self.task_context = self.context[name]
        self.task_context["start_time"] = datetime.now()
        self.task_context["name"] = name
        self.task_context["id"] = self.id
        self.task_context["activity_id"] = self.activity_id
        self.payload_task = payload[name]
        
        logger.info({
            "message": f"Executing service task:{name}",
            "data" : self.activity_data
        })

    def outgoing_flow_success(self,flow_id):
        context = self.context
        if context.get(flow_id) == None:
            context[flow_id] = {}

        context[flow_id]["start_time"] = datetime.now()        
        context[flow_id]["end_time"] = datetime.now()
        context[flow_id]["id"] = flow_id


    def get_outgoing_activities(self):
        
        outgoingflowid = self.activity_data.get("bpmn:outgoing")

        target_activity_id = None
        target_activity_type = None
        target_activity_data = None
        for seq_flow in self.process_instance.process_definition.get("bpmn:sequenceFlow"):
            if(seq_flow.get("@id") == outgoingflowid):
                self.outgoing_flow_success(outgoingflowid)
                target_activity_id = seq_flow.get("@targetRef")

        for component_name in self.process_instance.process_definition:
            
            if type(self.process_instance.process_definition[component_name]) == type(dict()):
                component = self.process_instance.process_definition[component_name]
                if component.get("@id") == target_activity_id:
                    target_activity_data = component
                    target_activity_type = component_name
            
            if type(self.process_instance.process_definition[component_name]) == type([]):
                for component in self.process_instance.process_definition[component_name]:
                    if component.get("@id") == target_activity_id:
                        target_activity_data = component
                        target_activity_type = component_name

        return [(target_activity_type,target_activity_id,target_activity_data)]
        