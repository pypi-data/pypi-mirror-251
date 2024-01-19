import typing

from tsproc.modules import Module, ProcModule, Process
from tsproc.context import ProcessContext, ModuleContext


class TestProcess(Process):
    def __init__(self, modules: typing.Tuple[Module, ...], context: typing.Optional[ProcessContext]):
        super().__init__(modules, context)


class TestSubProcess(Process):

    def __init__(self, modules: typing.Tuple[Module, ...], context: typing.Optional[ProcessContext]):
        super().__init__(modules, context)


class TestModule(ProcModule):

    def sync_module(self, process_context: ProcessContext, module_context: ModuleContext):
        module_context.number = process_context.number

    def execute_module(self, module_context: ModuleContext):
        module_context.number += 1

    def sync_process(self, process_context: ProcessContext, module_context: ModuleContext):
        process_context.number = module_context.number


class TestContext(ProcessContext):
    def __init__(self):
        super().__init__()
        self.number = 0
