import unittest

from tsproc.tests.test_process import TestProcess, TestContext, TestModule, TestSubProcess


class TestProcesses(unittest.TestCase):

    def test_process(self):
        modules = (
            TestModule(context=TestContext()),
            TestSubProcess(modules=(TestModule(context=TestContext()), TestModule(context=TestContext())),
                           context=None),
            TestModule(context=TestContext()),
        )
        context = TestContext()
        p = TestProcess(modules=modules, context=context)
        p(context=context)
        self.assertEqual(context.number, 4)
        self.assertEqual(context.number, len(p))
