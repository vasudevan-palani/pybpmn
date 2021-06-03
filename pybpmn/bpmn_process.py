from .bpmn_parser import BpmnParser
from .start_event import StartEvent
from .service_task import ServiceTask
from .user_task import UserTask
from .end_event import EndEvent
from .task import Task
from .exclusive_gateway import ExclusiveGateway
from .inclusive_gateway import InclusiveGateway
from .parallel_gateway import ParallelGateway
import uuid
from datetime import datetime, timezone
import logging

import concurrent.futures
import logging
from concurrent.futures import ThreadPoolExecutor


logger = logging.getLogger(__name__)

class BpmnProcess:
    def __init__(self):
        self.activities = []

    def start_process(self,process_definition,handler=None,context={}):
        parser = BpmnParser()
        self.process_definition = parser.load(process_definition)
        self.process_instance_id = str(uuid.uuid4())
        self.context = {
            "process_instance_id" : self.process_instance_id,
            "created_time" : datetime.now()
        }
        self.payload = context

        self.handler = handler

        self._start_execution()

    def set_payload(self,payload):
        self.payload = payload

    def _start_execution(self):
        self._execute_start_event()

    def _execute_start_event(self):
        start_event = StartEvent(self.process_definition.get("bpmn:startEvent",{}),self)
        start_event.execute(self.context,self.payload)

    def evaluate_results(self,results):
        if results == None:
            return
        activities = []
        for result in results:
            (activity_type,activity_id,activity_data) = result
            activity = self.get_activity_for_outgoing(activity_type,activity_id,activity_data)
            if activity :
                activities.append(activity)

        functions = []

        for activity in activities:
            # def function1():
            #     activity.execute(self.context,self.payload)
            functions.append((activity.execute,self.context,self.payload))

        if(len(activities) > 0):
            self.execute_parallel(len(activities),functions)


    def execute_parallel(self, workers, functions):
        results = []
        futures = []
        with ThreadPoolExecutor(max_workers=workers) as executor:
            for function_callable in functions:
                futures.append(executor.submit(*function_callable))

            concurrent.futures.wait(futures)

            for future in futures:
                results.append(future.result())
        return results

    def get_activity_for_outgoing(self,activity_type,activity_id,activity_data):
        for activity in self.activities:
            if hasattr(activity,"id") and activity.id == activity_id:
                return activity
    
        activity = None
        if(activity_type == "bpmn:serviceTask"):
            activity = ServiceTask(activity_data,self)
            self.activities.append(activity)

        if(activity_type == "bpmn:userTask"):
            activity = UserTask(activity_data,self)
            self.activities.append(activity)

        if(activity_type == "bpmn:exclusiveGateway"):
            activity = ExclusiveGateway(activity_data,self)
            self.activities.append(activity)

        if(activity_type == "bpmn:inclusiveGateway"):
            activity = InclusiveGateway(activity_data,self)
            self.activities.append(activity)

        if(activity_type == "bpmn:parallelGateway"):
            activity = ParallelGateway(activity_data,self)
            self.activities.append(activity)

        if(activity_type == "bpmn:endEvent"):
            activity = EndEvent(activity_data,self)
            self.activities.append(activity)

        return activity

        
    def get_activity_started(self):
        activities = []
        for activity in self.activities:
            if isinstance(activity,Task) and self.context.get(activity.name,{}).get("status") == "STARTED":
                activities.append(activity)

        return activities

    def _execute_task(self,task_name):
        getattr(self.handler, f'on_enter_{task_name}')(self)
        getattr(self.handler, f'on_{task_name}')()
        getattr(self.handler, f'on_exit_{task_name}')(self)

        if self.process_vars.get("task_name",{}).get("status",None) == "COMPLETE":
            self._complete_task(task_name)

    def get_activity_by_name(self,name):
        for activity_name in self.context:
            activity_dict = self.context[activity_name]
            if type(activity_dict) == type(dict()) and activity_dict.get("activity_id") != None and activity_name == name:
                for activity in self.activities:
                    if hasattr(activity,'activity_id') and activity.activity_id == activity_dict.get("activity_id"):
                        return activity

        return None

    def _get_start_task_name(self):
        return self.process_definition.get("bpmn:startEvent",{})