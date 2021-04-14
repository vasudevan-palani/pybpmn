import sys
sys.path.insert(0,".")

import logging.config
from loggingconfig import config as filelogconfig
logging.config.dictConfig(filelogconfig)

logger = logging.getLogger(__name__)

from pybpmn.bpmn_process import BpmnProcess
def test_asr_process():
    class Handler():
        def on_enter_task(self,**kargs):
            logger.info("Entering task")
        
        def on_exit_task(self,**kargs):
            logger.info("Exiting task")

        def on_enter_create_identity(self,**kargs):
            logger.info("Entering task create_identity")

        def on_create_identity(self,**kargs):
            context = kargs.get("context")
            context["user"] = True
            task_context = kargs.get("task")
            task_context.update({
                "name1" : "value1"
            })
            logger.info("Process task create_identity")

        def on_exit_create_identity(self,**kargs):
            logger.info("Exiting task create_identity")

        def on_enter_verify_identity(self,**kargs):
            logger.info("Entering task verify_identity")

        def on_verify_identity(self,**kargs):
            context = kargs.get("context")
            context["user"] = True
            task_context = kargs.get("task")
            task_context.update({
                "name1" : "value1"
            })
            logger.info("Process task verify_identity")

        def on_exit_verify_identity(self,**kargs):
            logger.info("Exiting task verify_identity")

        def on_enter_update_billing(self,**kargs):
            logger.info("Entering task update_billing")

        def on_update_billing(self,**kargs):
            context = kargs.get("context")
            context["user"] = True
            task_context = kargs.get("task")
            task_context.update({
                "name1" : "value1"
            })
            logger.info("Process task update_billing")

        def on_exit_update_billing(self,**kargs):
            logger.info("Exiting task update_billing")

        def on_enter_get_consent(self,**kargs):
            logger.info("Entering task get_consent")

        def on_get_consent(self,**kargs):
            context = kargs.get("context")
            context["user"] = True
            task_context = kargs.get("task")
            task_context.update({
                "name1" : "value1"
            })
            logger.info("Process task get_consent")

        def on_exit_get_consent(self,**kargs):
            logger.info("Exiting task get_consent")

    instance = BpmnProcess()
    instance.start_process(open("tests/data/test_asr.xml","r").read(),Handler(),{
        "asr_profile" : {
            "identity_creation_required" : True,
            "identity_verification_required" : True,
            "billing_required" : True,
            "consent_required" : True,
            "redirect_myaccount" : True
        }
    })
    instance.get_activity_by_name("create_identity").complete({"datatoadd":"Valuetoadd"})
    # instance.get_activity_by_name("verify_identity").complete({"datatoadd1":"Valuetoadd2"})
    # instance.get_activity_by_name("update_billing").complete({"datatoadd1":"Valuetoadd2"})
    # instance.get_activity_by_name("get_consent").complete({"datatoadd1":"Valuetoadd2"})