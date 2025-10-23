from typing import List, TypedDict, Union

class Input:
    size: int
    format: str

    def __init__(self, name: str, size = -1, format: str = "*"):
        self.name = name
        self.size = size
        self.format = format


class Option(TypedDict):
    value: str
    content: str

class OptionGroup():
    def __init__(self):
        self.options: List[Option] = []
    
    def add_option(self, option: Option):
        self.options.append(option)

class Select(TypedDict):
    name: str
    options: List[Union[Option, OptionGroup]]

class FieldSet(TypedDict):
    pass
