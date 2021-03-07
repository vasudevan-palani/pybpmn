import sys
sys.path.insert(0,".")

import logging.config
from loggingconfig import config as filelogconfig
logging.config.dictConfig(filelogconfig)

from pybpmn.bpmn_parser import BpmnParser
def test_parser():
    parser = BpmnParser()
    parser.load(open("tests/data/test_bpmn.xml","r").read())