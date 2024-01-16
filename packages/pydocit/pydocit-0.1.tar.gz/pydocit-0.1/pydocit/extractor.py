import inspect
from typing import Union, List
from types import ModuleType, FunctionType, CoroutineType, MethodType


def convert_annotations_into_str(annotation: dict) -> dict:
    new_annotations = {}
    for key, value in annotation.items():
        new_annotations[key] = value.__name__
    return new_annotations


def convert_default_values_into_str(defaults: dict) -> dict:
    stred_defaults = {}
    for key, value in defaults.items():
        stred_defaults[key] = str(value)
    return stred_defaults


class Error(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Imports:
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name


class Method:
    def __init__(self, meth: MethodType):
        self.meth: MethodType = meth
        self.__meth_name = self.meth.__name__

    @property
    def meth_name(self):
        return self.__meth_name

    def meth_declaration_definition(self):
        args_spec = inspect.getfullargspec(self.meth)
        annotations = convert_annotations_into_str(self.meth.__annotations__)

        default_parameters = None
        if args_spec.defaults is not None:
            default_parameters = dict(
                zip(args_spec.args[-len(args_spec.defaults) :], args_spec.defaults)
            )

        return {
            "args": args_spec.args,
            "annotations": annotations,
            "default_parameters": convert_default_values_into_str(default_parameters),
            "vargs": args_spec.varargs,
            "vkw": args_spec.varkw,
        }

    def get_final_docs(self) -> dict:
        doc_string = inspect.getdoc(self.meth)

        return {
            "name": self.meth_name,
            "doc_string": doc_string,
            "meth_declare_definition": self.meth_declaration_definition(),
        }


class Function:
    def __init__(self, func: Union[FunctionType, CoroutineType]):
        self.func = func
        self.__func_name = self.func.__name__
        if not isinstance(self.func, FunctionType):
            raise Error(f"Expected function type but got {type(self.func)}")

    @property
    def func_name(self):
        return self.__func_name

    def func_declaration_definition(self):
        args_spec = inspect.getfullargspec(self.func)
        annotations = convert_annotations_into_str(self.func.__annotations__)

        default_parameters = None
        if args_spec.defaults is not None:
            default_parameters = dict(
                zip(args_spec.args[-len(args_spec.defaults) :], args_spec.defaults)
            )

        return {
            "args": args_spec.args,
            "annotations": annotations,
            "default_parameters": convert_default_values_into_str(default_parameters),
            "vargs": args_spec.varargs,
            "vkw": args_spec.varkw,
        }

    def get_final_docs(self) -> dict:
        doc_string = inspect.getdoc(self.func)

        return {
            "name": self.func_name,
            "doc_string": doc_string,
            "func_declare_definition": self.func_declaration_definition(),
        }


class Class:
    def __init__(self, cls: type):
        self.cls = cls
        self.__cls_name = self.cls.__name__

        self.methods: List[Method] = []

        self.methods_docs = {}

        self.get_list_of_members()
        self.build_method_docs()

    @property
    def cls_name(self):
        return self.__cls_name

    def get_list_of_members(self):
        """Here the methods are considered function because
        the class is not initialized.

        Doesn't distinguish between classmethod, staticmethod, property,
        setter and getter.
        """
        for i in inspect.getmembers(self.cls):
            if isinstance(i[1], FunctionType):
                self.methods.append(Method(i[1]))

    def build_method_docs(self):
        for i in self.methods:
            self.methods_docs[i.meth_name] = i.get_final_docs()

    def get_final_docs(self) -> dict:
        doc_string = inspect.getdoc(self.cls)

        return {
            "name": self.cls_name,
            "methods": self.methods_docs,
            "doc_string": doc_string,
            "cls_declare_definition": " ",
        }


class Module:
    def __init__(self, mod: object) -> None:
        self.mod: object = mod
        self.imports: List[ModuleType] = []
        self.classes: List[Class] = []
        self.functions: List[Function] = []

        self.docs_classes = {}
        self.docs_functions = {}

        if isinstance(self.mod, ModuleType):
            self.module_members = inspect.getmembers(self.mod)
        else:
            raise Error(f"Expected module type but got {type(self.mod)}")

        self.sort_members()
        self.build_func_docs()
        self.build_classes_docs()

    def sort_members(self):
        # For now here members means function, classes and imports.

        # It only supports documentation only for functions, modules
        # and classes
        for i in self.module_members:
            if not isinstance(i[0], str):
                if not i[1].__module__ == self.mod.__name__:
                    continue
            if inspect.isfunction(i[1]):
                self.functions.append(Function(i[1]))
            elif inspect.ismodule(i[1]):
                self.imports.append(i[1])
            elif inspect.isclass(i[1]):
                self.classes.append(Class(i[1]))

    def build_func_docs(self):
        for i in self.functions:
            docs = i.get_final_docs()
            self.docs_functions[i.func_name] = docs

    def build_classes_docs(self):
        for i in self.classes:
            docs = i.get_final_docs()
            self.docs_classes[i.cls_name] = docs

    def get_final_docs(self):
        doc_string = inspect.getdoc(self.mod)

        return {
            "imports": self.imports,
            "classes": self.docs_classes,
            "functions": self.docs_functions,
            "doc_string": doc_string,
        }
