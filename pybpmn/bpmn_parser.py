import logging
import xmltodict
import json
logger = logging.getLogger(__name__)

class BpmnParser:

    def get_target_flow_by_id(self,seq_flows,seq_flow_id):
        for flow_dict in seq_flows:
            if flow_dict.get("@id") == seq_flow_id:
                return flow_dict.get("@targetRef")

    def load(self,process_definition):
        final_definition = {}
        json_process_definition = xmltodict.parse(process_definition)
        return json.loads(json.dumps(json_process_definition.get("bpmn:definitions",{}).get("bpmn:process",{})))