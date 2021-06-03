import sys
sys.path.insert(0,".")

import logging.config
from loggingconfig import config as filelogconfig
logging.config.dictConfig(filelogconfig)

logger = logging.getLogger(__name__)

import time

from pybpmn.bpmn_process import BpmnProcess
class Handler():
    def on_enter_task(self,**kargs):
        logger.info("Entering task")
    
    def on_exit_task(self,**kargs):
        logger.info("Exiting task")

    def on_enter_task_2(self,**kargs):
        logger.info("Entering task task_2")

    def on_task_2(self,**kargs):
        context = kargs.get("context")
        payload = kargs.get("payload")
        payload["user"] = True
        task_context = kargs.get("task")
        task_context.update({
            "name1" : "value1"
        })
        logger.info("Process task task_2")

    def on_exit_task_2(self,**kargs):
        logger.info("Exiting task task_2")

    def on_enter_task_3(self,**kargs):
        logger.info("Entering task task_3")

    def on_task_3(self,**kargs):
        logger.info("Process task task_3")

    def on_exit_task_3(self,**kargs):
        logger.info("Exiting task task_3")

    def on_enter_task_4(self,**kargs):
        logger.info("Entering task task_4")

    def on_task_4(self,**kargs):
        time.sleep(3)
        logger.info("Process task task_4")

    def on_exit_task_4(self,**kargs):
        logger.info("Exiting task task_4")

    def on_enter_task_5(self,**kargs):
        logger.info("Entering task task_5")

    def on_task_5(self,**kargs):
        time.sleep(5)
        context = kargs.get("context")
        context["user"] = True
        task_context = kargs.get("task")
        task_context.update({
            "name1" : "value1"
        })
        logger.info("Process task task_5")

    def on_exit_task_5(self,**kargs):
        logger.info("Exiting task task_5")

    def on_enter_task_6(self,**kargs):
        logger.info("Entering task task_6")

    def on_exit_task_6(self,**kargs):
        logger.info("Exiting task task_6")
def test_process():

    instance = BpmnProcess()
    instance.start_process(open("tests/data/test_bpmn.xml","r").read(),Handler())
    instance.get_activity_by_name("task_3").complete({"datatoadd":"Valuetoadd"})
    instance.get_activity_by_name("task_5").complete({"datatoadd1":"Valuetoadd2"})
    import pickle
    pickle.dump(instance,open( "save.p", "wb" ))

def test_parallel_gw_process():

    instance = BpmnProcess()
    instance.start_process(open("tests/data/test_bpmn_parallel_gw.xml","r").read(),Handler())
    time.sleep(5)
    instance.get_activity_by_name("task_3").complete({"datatoadd":"Valuetoadd"})
    instance.get_activity_by_name("task_5").complete({"datatoadd1":"Valuetoadd2"})
    import pickle
    pickle.dump(instance,open( "save.p", "wb" ))


def test_incl_gw_process():

    instance = BpmnProcess()
    instance.start_process(open("tests/data/test_bpmn_incl_gw.xml","r").read(),Handler())
    time.sleep(5)
    instance.get_activity_by_name("task_3").complete({"datatoadd":"Valuetoadd"})
    instance.get_activity_by_name("task_5").complete({"datatoadd1":"Valuetoadd2"})
    instance.get_activity_by_name("task_6").complete({"datatoadd1":"Valuetoadd2"})
    import pickle
    pickle.dump(instance,open( "save.p", "wb" ))