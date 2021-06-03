# pybpmn

## Introduction

BPMN is a notation to describe a business process. The implementation and execution of the business process can be done with various technologies. As technologies evolve, the implementation becomes more easier to adopt and maintain. This python module implements some basics BPMN features for cloud to keep the things as simple as possible.


## Design approach
- The bpmn process is backed by a python handler class to realize the desired functionality.
- Generic on_enter_task and on_exit_task callbacks are available
- task specific on_enter_<task_name> , on_exit_<task_name> and on_<task_name> could be implemented to get callbacks from the module

Sample code is as shown below

```python
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
```

## Supported features

### Events

The below list of events are currently supported. 
- start
- end


### Tasks

#### Service Task

These are automated tasks which are pure functions which does desired functionality.

#### User Task

These are user tasks, the main difference between user and service tasks is, user tasks are required to be completed explicity to move the token in the process. Tasks can be completed by using the code as shown below

```python
instance.get_activity_by_name("task_3").complete({"datatoadd":"Valuetoadd"})
```
### Gateways

#### Exclusive gateway
Exclusive gateways could be diverging or converging. For diverging gateway, only one path should evaluate to true or first path that gets evaluated to true, will be the path the bpmn process will take. Path's with no conditional expression ( python ) is considered to be 'True'

For converging gateways, atleast one incoming pathways will move the token up the process.

### Inclusive gateway
Inclusive gateways again could be diverging or converging. These gateways by definition, will allow more than one pathways to be taken during process execution. All paths whose conditional expression evaluates to true OR doesnt have an expression will be chosen for execution. All paths will be executed in parallel until a blocking task is encountered.

For coverging gateways, the naming convention should be conv_<diverging_pair_name>. The inclusive gateway will await for as many as diverged paths to proceed execution of process.

### Parallel gateway

Parallel gateways will execute all diverging paths, and awaits every converging path in the process.

