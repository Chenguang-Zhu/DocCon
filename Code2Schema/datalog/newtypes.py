from typing import NewType, TypeVar


ContractName = NewType("ContractName", str)
FunctionName = NewType("FunctionName", str)
Event = NewType("Event", str)
Param = NewType("Param", str)
SVar = NewType("SVar", str)
CtMod = NewType("CtMod", str)
FnMod = NewType("FnMod", str)
SouffleListItem = TypeVar("SouffleListItem")