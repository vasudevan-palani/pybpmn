import sys
sys.path.insert(0,".")

import logging.config
from loggingconfig import config as filelogconfig
logging.config.dictConfig(filelogconfig)

logger = logging.getLogger(__name__)

from pybpmn.bpmn_process import BpmnProcess
def test_process():
    class Handler():
        def on_enter_task(self,**kargs):
            logger.info("Entering task")
        
        def on_exit_task(self,**kargs):
            logger.info("Exiting task")

        def on_enter_task_2(self,**kargs):
            logger.info("Entering task task_2")

        def on_task_2(self,**kargs):
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

    instance = BpmnProcess()
    instance.start_process(open("tests/data/test_bpmn.xml","r").read(),Handler())
    act_id = instance.get_activity_by_name("task_3")
    instance.complete_task(act_id,{"datatoadd":"Valuetoadd"})
    