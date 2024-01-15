# -*- coding: utf-8 -*-
import inspect
from types import ModuleType
from typing import Type, List, TypeVar
from importlib import import_module


T = TypeVar('T')


def find_all_subclasses(module: str | ModuleType, base_class: Type[T]) -> List[Type[T]]:
    if isinstance(module, str):
        module = import_module(module)

    all_class_list = list()
    for name in dir(module):
        obj = getattr(module, name)
        if inspect.isclass(obj):
            all_class_list.append(obj)

    all_subclass_list = list()
    for the_class in all_class_list:
        if issubclass(the_class, base_class) and the_class != base_class:
            all_subclass_list.append(the_class)

    return all_subclass_list
