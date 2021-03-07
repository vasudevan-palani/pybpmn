import abc
from .gateway import Gateway
from datetime import datetime

import logging

logger = logging.getLogger(__name__)

class ExclusiveGateway(Gateway):
    
    def execute(self,context):
        self._execute(context)
        name = self.name
        task = self.task_context
        
        # getattr(self.process_instance.handler,f"on_enter_task")(context = context,task = task)
        # getattr(self.process_instance.handler,f"on_enter_{name}")(context = context,task = task)
        # getattr(self.process_instance.handler,f"on_{name}")(context = context,task = task)
        # getattr(self.process_instance.handler,f"on_exit_{name}")(context = context,task = task)
        # getattr(self.process_instance.handler,f"on_exit_task")(context = context,task = task)
        context[name]["end_time"] = datetime.now()
        
        self.process_instance.evaluate_results(self.get_outgoing_activities())


    def get_outgoing_activities(self):
        context = self.context
        outgoingflowids = self.activity_data.get("bpmn:outgoing")
        target_activity_ids=[]
        if type(outgoingflowids) == type([]):
            for outgoingflowid in outgoingflowids:
                for seq_flow in self.process_instance.process_definition.get("bpmn:sequenceFlow"):
                    if(seq_flow.get("@id") == outgoingflowid):
                        if seq_flow.get("bpmn:conditionExpression",{}).get("#text") != None:
                            if eval(seq_flow.get("bpmn:conditionExpression",{}).get("#text")) == True:
                                target_activity_ids.append(seq_flow.get("@targetRef"))                
                        

        targets = []

        logger.info(target_activity_ids)

        for target_activity_id in target_activity_ids:
            for component_name in self.process_instance.process_definition:
                if type(self.process_instance.process_definition[component_name]) == type(dict()):
                    component = self.process_instance.process_definition[component_name]
                    if component.get("@id") == target_activity_id:
                        target_activity_data = component
                        target_activity_type = component_name

                        targets.append((target_activity_type,target_activity_id,target_activity_data))

                if type(self.process_instance.process_definition[component_name]) == type([]):
                    for component in self.process_instance.process_definition[component_name]:
                        if component.get("@id") == target_activity_id:
                            target_activity_data = component
                            target_activity_type = component_name
                            targets.append((target_activity_type,target_activity_id,target_activity_data))


        return targets