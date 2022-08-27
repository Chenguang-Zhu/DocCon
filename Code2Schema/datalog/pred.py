from pyclbr import Function
from typing import NamedTuple

from datalog.dlexpr import Expr, SouffleList
from datalog.newtypes import ContractName, FunctionName, Event, Param, SVar, CtMod, FnMod


class HasFnFact(NamedTuple):
    ct: ContractName
    fn: FunctionName

    def __str__(self):
        return f"{self.ct}\t{self.fn}"


class HasParamFact(NamedTuple):
    ct: ContractName
    fn: FunctionName
    p: Param

    def __str__(self):
        return f"{self.ct}\t{self.fn}\t{self.p}"


class SeeFnFact(NamedTuple):
    cur_ct: ContractName
    cur_fn: FunctionName
    target_ct: ContractName
    target_fn: FunctionName

    def __str__(self):
        return f"{self.cur_ct}\t{self.cur_fn}\t{self.target_ct}\t{self.target_fn}"


class RequireFact(NamedTuple):
    ct: ContractName
    fn: FunctionName
    condition: Expr

    def __str__(self):
        return f"{self.ct}\t{self.fn}\t{self.condition}"


class EmitFact(NamedTuple):
    ct: ContractName
    fn: FunctionName
    event: Event
    condition: Expr

    def __str__(self):
        return f"{self.ct}\t{self.fn}\t{self.event}\t{self.condition}"


class RevertFact(NamedTuple):
    ct: ContractName
    fn: FunctionName
    condition: Expr

    def __str__(self):
        return f"{self.ct}\t{self.fn}\t{self.condition}"


class IsContractFact(NamedTuple):
    """
    Write facts to "isContract.facts"
    """
    ct: ContractName

    def __str__(self):
        return f"{self.ct}"

class IsInterfaceFact(NamedTuple):
    """
    Write facts to "isInterface.facts"
    """
    ct: ContractName

    def __str__(self):
        return f"{self.ct}"


class InheritFact(NamedTuple):
    """
    Write facts to "Inherit.facts"
    """
    parent_ct: ContractName
    child_ct: ContractName

    def __str__(self):
        return f"{self.parent_ct}\t{self.child_ct}"


class OverrideFact(NamedTuple):
    """
    Write facts to "Override.facts"
    """
    parent_ct: ContractName
    parent_fn: FunctionName
    child_ct: ContractName
    child_fn: FunctionName

    def __str__(self):
        return f"{self.parent_ct}\t{self.parent_fn}\t{self.child_ct}\t{self.child_fn}"

class IsImplementedFact(NamedTuple):
    """
    Write facts to "IsImplemented.facts"
    """
    ct: ContractName
    fn: FunctionName

    def __str__(self) -> str:
        return f"{self.ct}\t{self.fn}"

class StateVarFact(NamedTuple):
    """
    Write facts to "HasStateVar.facts"
    """
    ct: ContractName
    state_var: SVar

    def __str__(self):
        return f"{self.ct}\t{self.state_var}"


class CtModFact(NamedTuple):
    """
    Write facts to "CtHasMod.facts"
    """
    ct: ContractName
    mod: CtMod

    def __str__(self):
        return f"{self.ct}\t{self.mod}"


class FnModFact(NamedTuple):
    """
    Write facts to "FnHasMod.facts"
    """
    ct: ContractName
    fn: FunctionName
    mod: FnMod

    def __str__(self):
        return f"{self.ct}\t{self.fn}\t{self.mod}"


class CallFact(NamedTuple):
    """
    Write facts to "Call.facts"
    """
    ct_caller: ContractName
    caller: FunctionName
    actual_args: SouffleList
    ct_callee: ContractName
    callee: FunctionName
    params: SouffleList

    def __str__(self):
        return f"{self.ct_caller}\t{self.caller}\t{self.actual_args}\t" \
               f"{self.ct_callee}\t{self.callee}\t{self.params}"


class DefinedFunctionFact(NamedTuple):
    """
    Write facts to "DefinedFunction.facts"
    """
    ct: ContractName
    fn: FunctionName
    def __str__(self) -> str:
        return f"{self.ct}\t{self.fn}"