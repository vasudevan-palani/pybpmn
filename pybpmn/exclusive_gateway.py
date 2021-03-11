import abc
from .gateway import Gateway
from datetime import datetime

import logging

logger = logging.getLogger(__name__)

class ExclusiveGateway(Gateway):
    
    def execute(self,context,payload):
        self._execute(context,payload)
        name = self.name
        task = self.task_context
        
        context[name]["start_time"] = datetime.now()        
        context[name]["end_time"] = datetime.now()
        self.process_instance.evaluate_results(self.get_outgoing_activities())

    def outgoing_flow_success(self,flow_id):
        context = self.context
        if context.get(flow_id) == None:
            context[flow_id] = {}

        context[flow_id]["start_time"] = datetime.now()        
        context[flow_id]["end_time"] = datetime.now()
        context[flow_id]["id"] = flow_id

    def is_atleast_one_incoming_complete(self):
        incomingflowids = self.activity_data.get("bpmn:incoming")
        source_activity_refs=[]
        if type(incomingflowids) == type([]):
            for incomingflowid in incomingflowids:
                for seq_flow in self.process_instance.process_definition.get("bpmn:sequenceFlow"):
                    if(seq_flow.get("@id") == incomingflowid):
                        source_activity_refs.append(seq_flow.get("@sourceRef"))

        source_activity_names = []
        for source_activity_ref in source_activity_refs:
            for component_name in self.process_instance.process_definition:
                if type(self.process_instance.process_definition[component_name]) == type(dict()):
                    component = self.process_instance.process_definition[component_name]
                    if component.get("@id") == source_activity_ref:
                        source_activity_names.append(component.get("@name"))

                if type(self.process_instance.process_definition[component_name]) == type([]):
                    for component in self.process_instance.process_definition[component_name]:
                        if component.get("@id") == source_activity_ref:
                            source_activity_names.append(component.get("@name"))

        for source_activity_name in source_activity_names:
            if(self.context.get(source_activity_name,{}).get("status") == "COMPLETED"):
                return True

        return False

    def is_all_incoming_complete(self):
        incomingflowids = self.activity_data.get("bpmn:incoming")
        source_activity_refs=[]
        if type(incomingflowids) == type([]):
            for incomingflowid in incomingflowids:
                for seq_flow in self.process_instance.process_definition.get("bpmn:sequenceFlow"):
                    if(seq_flow.get("@id") == incomingflowid):
                        source_activity_refs.append(seq_flow.get("@sourceRef"))

        source_activity_names = []
        for source_activity_ref in source_activity_refs:
            for component_name in self.process_instance.process_definition:
                if type(self.process_instance.process_definition[component_name]) == type(dict()):
                    component = self.process_instance.process_definition[component_name]
                    if component.get("@id") == source_activity_ref:
                        source_activity_names.append(component.get("@name"))

                if type(self.process_instance.process_definition[component_name]) == type([]):
                    for component in self.process_instance.process_definition[component_name]:
                        if component.get("@id") == source_activity_ref:
                            source_activity_names.append(component.get("@name"))

        for source_activity_name in source_activity_names:
            if(self.context.get(source_activity_name,{}).get("status","NOT_DEFINED") != "COMPLETED"):
                return False

        return True

    def get_outgoing_activities(self):
        context = self.context
        payload = self.payload
        outgoingflowids = self.activity_data.get("bpmn:outgoing")
        
        if type(outgoingflowids) != type([]):
            outgoingflowids = [outgoingflowids]

        target_activity_ids=[]
        if type(outgoingflowids) == type([]):
            for outgoingflowid in outgoingflowids:
                for seq_flow in self.process_instance.process_definition.get("bpmn:sequenceFlow"):
                    if(seq_flow.get("@id") == outgoingflowid):
                        if seq_flow.get("bpmn:conditionExpression",{}).get("#text") != None:
                            if eval(seq_flow.get("bpmn:conditionExpression",{}).get("#text")) == True:
                                target_activity_ids.append(seq_flow.get("@targetRef"))
                                self.outgoing_flow_success(outgoingflowid)
                        else:
                            target_activity_ids.append(seq_flow.get("@targetRef"))
                            self.outgoing_flow_success(outgoingflowid)
                        

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