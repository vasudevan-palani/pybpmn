import abc
from .gateway import Gateway
from datetime import datetime

import logging

logger = logging.getLogger(__name__)

class InclusiveGateway(Gateway):
    """ Inclusive gateway implementation

        If this gateway needs to be used as convergence gateway, The name of the gateway should match conv_{diverging_gateway_name}
    """
    def execute(self,context,payload):
        self._execute(context,payload)
        name = self.name
        task = self.task_context
        
        context[name]["start_time"] = datetime.now()        
        context[name]["end_time"] = datetime.now()

        self.payload_task = payload[name]
        payload_task = self.payload_task

        if self.process_instance.handler != None:
            if hasattr(self.process_instance.handler,f"on_enter_{name}"):
                getattr(self.process_instance.handler,f"on_enter_{name}")(context = context,task = payload_task, payload = payload, process_instance = self.process_instance)

        self.process_instance.evaluate_results(self.get_outgoing_activities())

    def outgoing_flow_success(self,flow_id):
        context = self.context
        if context.get(flow_id) == None:
            context[flow_id] = {}

        context[flow_id]["start_time"] = datetime.now()        
        context[flow_id]["end_time"] = datetime.now()
        context[flow_id]["id"] = flow_id

    def is_converge_gateway(self):
        incomingflowids = self.activity_data.get("bpmn:incoming")
        outgoingflowids = self.activity_data.get("bpmn:outgoing")

        if(type(incomingflowids) != type([])):
            incomingflowids = [incomingflowids]
        
        if(type(outgoingflowids) != type([])):
            outgoingflowids = [outgoingflowids]

        if len(incomingflowids) > 1 and len(outgoingflowids) == 1:
            return True

        return False

    def is_converge_complete(self):
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

        complete_count = 0
        for source_activity_name in source_activity_names:
            if(self.context.get(source_activity_name,{}).get("status","NOT_DEFINED") == "COMPLETED"):
                complete_count = complete_count + 1

        if len(self.context.get(self.name.replace("conv_",""),{}).get("success_paths",[])) == complete_count:
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

        complete_count = 0
        for source_activity_name in source_activity_names:
            if(self.context.get(source_activity_name,{}).get("status","NOT_DEFINED") == "COMPLETED"):
                complete_count = complete_count + 1

        if len(self.context.get(self.name.replace("conv_",""),{}).get("success_paths",[])) == complete_count:
            return True
        
        return False

    def get_outgoing_activities(self):

        # If this is a converge gateway, wait for all execution paths to converge
        #
        if self.is_converge_gateway() == True and self.is_converge_complete() != True:
            return None

        # If the gateway is a diverge gateway
        #
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


        self.context[self.name]["success_paths"] = targets
        return targets