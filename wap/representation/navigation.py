from enum import StrEnum
from typing import List, TypedDict, Union

from wap.representation.html.text import TextContent
from wap.representation.variables import SetVarElement

class OnPick():
    pass

class HttpMethod(StrEnum):
    get = "get"
    post = "post"

class GoElement():
    def __init__(self, href: str, method = HttpMethod.get):
        self.href = href
        self.method = method
    
    def method_from_str(self, input: str):
        getattr(HttpMethod, input, HttpMethod.get)

    def activate():
        pass

class PrevElement():
    def activate():
        pass

class RefreshElement():
    def __init__(self, effect: SetVarElement):
        self.effect = effect

    def activate(self):
        self.effect.activate()

class Do():
    type: str
    label: str

class NoOpElement():
    def activate(self):
        pass

class AnchorElement(TypedDict):
    children:  List[Union[TextContent, GoElement, PrevElement, RefreshElement]]

class EventType(StrEnum):
    """
    Actions that can be triggered when the user browses or interacts with a card
    on_enter_backward: User enters card by normal backward navigation
    on_enter_forward: User enters card by normal forward navigation
    onpick: User select an option
    on_timer: Activated when timer is expires
    """
    on_enter_backward = "onenterbackward"
    on_enter_forward = "onenterforward"
    on_timer = "ontimer"

class OnEvent():
    def __init__(self, type: str, action: Union[GoElement, PrevElement, RefreshElement]):
        self.type = type
        self.action = action