import os
import unittest
from os.path import dirname

from ronds_sdk.parser.dag_parser import RuleBaseDagParser
from ronds_sdk.tools import utils


class ArgParserTest(unittest.TestCase):

    def test_get_dag(self):
        arg_file = '%s/arg.txt' % dirname(dirname(os.getcwd()))
        arg_parse = RuleBaseDagParser(arg_file)
        p = arg_parse.pipeline()
        self.assertTrue(len(p.graph.nodes) > 0)
        utils.draw_graph(p.graph)
        p.run().wait_until_finish()
