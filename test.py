import sys
sys.path.append("./src")
from summer import *

@Bean(name="vasu")
class A():
    def __init__(self):
        pass

    def sayHi(self):
        print("Hi from A")


@Bean()
class Logger():
    def __init__(self):
        pass

    def sayHi(self):
        print("Hi from logger")


@Bean(name="vasu1")
class B():
    def __init__(self):
        pass

    @Autowired()
    def sayHi(self,logger1:Logger):
        logger1.sayHi()

class Test1():
    def __init__(self):
        pass

    #@Bean(name="test")
    def getBean(self):
        return A()

context.initialize()
b = context.getClassByName("vasu1")
b.sayHi()
