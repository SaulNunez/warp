from typing import TypedDict


class SetVarElement(TypedDict):
    name: str
    value: str
    data_class: str

class TimerElement(TypedDict):
    value: str