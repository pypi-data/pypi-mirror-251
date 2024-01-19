import abc
import typing

from tsproc.context import ProcessContext, ModuleContext


class Module(abc.ABC):

    def __init__(self, context: ModuleContext):
        self._context = context

    @property
    def context(self):
        return self._context

    @abc.abstractmethod
    def run(self, process_context: ProcessContext, module_context: ModuleContext):
        pass

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}"

    def __len__(self):
        return 1


class ProcModule(Module):

    # TODO python 3.8 add @final
    def run(self, process_context: ProcessContext, module_context: ModuleContext):
        self.sync_module(process_context=process_context, module_context=module_context)
        self.execute_module(module_context=module_context)
        self.sync_process(process_context=process_context, module_context=module_context)

    @abc.abstractmethod
    def sync_module(self, process_context: ProcessContext, module_context: ModuleContext):
        pass

    @abc.abstractmethod
    def execute_module(self, module_context: ModuleContext):
        pass

    @abc.abstractmethod
    def sync_process(self, process_context: ProcessContext, module_context: ModuleContext):
        pass


class Process(Module):

    def __init__(self, modules: typing.Tuple[Module, ...], process_context: ProcessContext):
        super().__init__(process_context)
        self._modules = modules

    @property
    def modules(self):
        return self._modules

    # TODO python 3.8 add @final
    def run(self, process_context: ProcessContext, module_context: ModuleContext = None):
        for module in self:
            module_context = module.context
            module.run(process_context=process_context, module_context=module_context)

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"{class_name}({[m for m in self]})"

    def __len__(self):
        return sum(len(m) for m in self)

    def __call__(self, context: ProcessContext):
        self.run(context, module_context=None)

    def __getitem__(self, index):
        return self._modules[index]
