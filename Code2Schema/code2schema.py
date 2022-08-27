
import os 
from typing import Optional, Set
import json
from black import err

from slither.core.cfg.node import NodeType

from slither.core.declarations import (
        Function,
        SolidityFunction,
        Contract,
        SolidityVariable,
    )
from slither.core.variables.variable import Variable
from slither.core.expressions.assignment_operation import AssignmentOperation
from slither.core.expressions.binary_operation import BinaryOperation
from slither.core.expressions.call_expression import CallExpression
from slither.core.expressions.conditional_expression import ConditionalExpression
from slither.core.expressions.elementary_type_name_expression import ElementaryTypeNameExpression
from slither.core.expressions.expression import Expression
from slither.core.expressions.identifier import Identifier
from slither.core.expressions.index_access import IndexAccess
from slither.core.expressions.literal import Literal
from slither.core.expressions.member_access import MemberAccess
from slither.core.expressions.new_array import NewArray
from slither.core.expressions.new_contract import NewContract
from slither.core.expressions.new_elementary_type import NewElementaryType
from slither.core.expressions.tuple_expression import TupleExpression
from slither.core.expressions.type_conversion import TypeConversion
from slither.core.expressions.unary_operation import UnaryOperation
from slither.exceptions import SlitherError
from slither.slithir.operations.event_call import EventCall
from transitive import OVERRIDENFUNCS_FACTS, buildTransitive
from util import conds2Expr
from datalog.dlexpr import Expr, SouffleList, Bool
from datalog.pred import HasFnFact, RequireFact, EmitFact, RevertFact, HasParamFact

from datalog.pred import CtModFact,  FnModFact, InheritFact, OverrideFact, CallFact, StateVarFact, IsContractFact, IsInterfaceFact, IsImplementedFact

def processStateVariables(contractname, statevariables):
    hasStateVariables = []
    for statevariable in statevariables:
        hasStateVariables.append((contractname, statevariable.name))
    return hasStateVariables

def processFunctionParameters(funcName, params):
    hasParams = []
    for param in params:
        hasParams.append((funcName, param.name))
    return hasParams

EQ = "=="
NEQ = "!="
GT = ">"
GEQ = ">="
LT = "<"
LEQ = "<="
AND = "&&"
OR = "||"
NOT = "!"
ADD = "+"
SUB = "-"
MULTIPLY = "*"
DIVIDE = "/"
MOD = "%"

def translateOpType(opType):
    if opType == EQ:
        return "EQ"
    elif opType == NEQ:
        return "NEQ"
    elif opType == GT:
        return "GT"
    elif opType == GEQ:
        return  "GEQ"
    elif opType == LT:
        return "LT"
    elif opType == LEQ:
        return "LEQ"
    elif opType == AND:
        return "AND"
    elif opType == OR:
        return "OR"
    elif opType == NOT:
        return "NOT"
    elif opType == ADD:
        return "ADD"
    elif opType == SUB:
        return "SUB"
    elif opType == MULTIPLY:
        return "MUL"
    elif opType == DIVIDE:
        return "DIV"
    elif opType == MOD:
        return "MOD"
    else:
        print(opType)
        assert False  

def processCondition(booleanExpression):
    result = []
    if isinstance(booleanExpression, BinaryOperation):
        opType = translateOpType(str(booleanExpression.type)) 
        left = processCondition(booleanExpression.expression_left)
        right = processCondition(booleanExpression.expression_right)
        result.append(str(opType))
        result.extend(left)
        result.extend(right)
        return result 
    elif isinstance(booleanExpression, Literal):
        result.append(str(booleanExpression))
        return result 
    elif isinstance(booleanExpression, TypeConversion):
        result.append(str(booleanExpression))
        return result
    elif isinstance(booleanExpression, CallExpression):
        result.append(str(booleanExpression))
        return result
    elif isinstance(booleanExpression, UnaryOperation):
        opType = translateOpType(str(booleanExpression.type)) 
        exp = booleanExpression.expression
        result.append(str(opType))
        result.append(str(exp))
        return result
    else:
        result.append(str(booleanExpression).replace(" ", ""))
        return result

def processRequire(function):
    hasRequire = []
    for node in function.nodes:
        isRequireOrAssert = node.contains_require_or_assert()
        if isRequireOrAssert:
            readStateVariables = node.state_variables_read
            readLocalVariables = node.local_variables_read 
            readSolidityVariables = node.solidity_variables_read
            if node.expression is not None:
                # print(node.expression)
                requireArguments = node.expression.arguments
                condition = requireArguments[0]
                result = processCondition(condition)
                # print(" ".join(result))
                errorMsg = None 
                if len(requireArguments)>1:
                    errorMsg = requireArguments[1]
                # varnames = [ variable.name for variable in readStateVariables]
                # varnames.extend([ variable.name for variable in readLocalVariables])
                # varnames.extend([ variable.name for variable in readSolidityVariables])
                # hasRequire.append([function.name, varnames])
                req_item = [function.name]
                req_item.extend(result)
                hasRequire.append(req_item)
    return hasRequire


def processEvents(function):
    hasEvents = []
    hasIfEvents = []
    for node in function.nodes:
        isIf = node.contains_if(include_loop=True)
        if not isIf:
            for ir in node.irs:
                if isinstance(ir, EventCall):
                    hasEvents.append((function.name, ir.name)) 
        else:
            booleanExpression = node.expression
            result = processCondition(booleanExpression=booleanExpression)
            trueNode =  node.son_true
            falseNode = node.son_false
            if (trueNode is not None):
                for ir in trueNode.irs:
                    if isinstance(ir, EventCall):
                        hasIfEvents.append((function.name, ir.name)) 
                        
        # if any(ir for node in function.nodes for ir in node.irs if isinstance(ir, EventCall)):
                # continue
    return hasEvents, hasIfEvents


def processIFREVERTs(function):
    hasIfReverts = []
    hasIfNotReverts = []
    for node in function.nodes:
        isIf = node.contains_if(include_loop=False)
        if isIf:
            booleanExpression = node.expression
            result = processCondition(booleanExpression=booleanExpression)
            trueNode =  node.son_true
            falseNode = node.son_false
            if (trueNode is not None and trueNode.type == NodeType.THROW):
                # readStateVariables = node.state_variables_read
                # readLocalVariables = node.local_variables_read 
                # varnames = [ variable.name for variable in readStateVariables]
                # varnames.extend([ variable.name for variable in readLocalVariables])
                req_item = [function.name]
                req_item.extend(result)
                hasIfReverts.append(req_item)
            elif (falseNode is not None and falseNode.type == NodeType.THROW):
                req_item = [function.name]
                req_item.extend(result)
                hasIfNotReverts.append(req_item)
            
    return hasIfReverts, hasIfNotReverts

from slither.slithir.operations.high_level_call import HighLevelCall
from slither.slithir.operations.internal_call import InternalCall
from slither.slithir.operations.library_call import LibraryCall
from slither.core.cfg.node import Node
from datalog.newtypes import Param
def processHighLevelCalls(fnName: str, node: Node):
    highLevelCalls = []
    for ir in node.irs:
        if isinstance(ir, HighLevelCall) and not isinstance(ir, LibraryCall):
            if isinstance(ir.destination.type, Contract):
                highLevelCalls.append([fnName, ir.arguments, ir.destination.type.name, ir.function.name, ir.function.parameters])
            elif ir.destination == SolidityVariable("this"):
                # call to other functions insides the same contract
                highLevelCalls.append([fnName, ir.arguments, ir.function.name, ir.function.parameters])
            else: 
                try:
                    highLevelCalls.append([fnName, ir.arguments, ir.destination.type.type.name, ir.function.name,  ir.function.parameters])
                except AttributeError as error:
                    err(error)
                # if fnName == "_asyncTransfer":
                #     print(highLevelCalls)
                #     print(ir)
                #     exit(0)
        elif isinstance(ir, LibraryCall):
                assert isinstance(ir.destination, Contract)
                highLevelCalls.append([fnName, ir.arguments, ir.destination.name, ir.function.name, ir.function.parameters])
        else:
            pass 
     
    return highLevelCalls

def processInternalCalls(fnName: str, node: Node):
    internalCalls = []
    for ir in node.irs:
        if isinstance(ir, InternalCall):
            # call to other functions insides the same contract
            internalCalls.append([fnName, ir.arguments, ir.function.name, ir.function.parameters])
    return internalCalls

def processFunctionCall(function):
    hasFunctionCalls = []

    hasFunctionCalls_full = [] 
    for node in function.nodes:
        hasFunctionCalls_full.extend(processHighLevelCalls(function.name, node))
        hasFunctionCalls_full.extend(processInternalCalls(function.name, node))


    for call in function.high_level_calls:
        contract, functionorvar = call
        if isinstance(functionorvar, Function) and functionorvar != function: 
            contractName = contract.name 
            funcName = functionorvar.name
            hasFunctionCalls.append([function.name, contractName, funcName])
    
    for call in function.internal_calls:
        functionorsolidityfunction = call
        if isinstance(functionorsolidityfunction, Function) and functionorsolidityfunction != function: 
            funcName = functionorsolidityfunction.name
            hasFunctionCalls.append([function.name, funcName])
        # if any(ir for node in function.nodes for ir in node.irs if isinstance(ir, EventCall)):
                # continue
    return hasFunctionCalls, hasFunctionCalls_full


def processFunctionOverride(contract, function):
    hasOverride_funcs = []
    overriden_funcs = contract.get_functions_overridden_by(function) 
    for overriden_func in overriden_funcs:
         for c in contract.inheritance:
             if overriden_func in c.functions_declared:
                 hasOverride_funcs.append([function.name, c.name, function.name])
    return hasOverride_funcs

def processUseModifiers(function):
    useModifiers = []
    for modifier in function.modifiers:
        if isinstance(modifier, Function):
            useModifiers.append([function.name, modifier.name])
    return useModifiers

def code2Schema(slither, args):
    # print(slither.filename)
    index = 0
    factsdir = args.factsdir 
    if not os.path.exists(factsdir):
        os.makedirs(factsdir)
    # print("Index\t Contract\t No. Functions \t No. Modifiers \t No. State Variables")
    funcParam = dict()

    hasFn_facts_dl: Set[HasFnFact] = set()
    hasParam_facts_dl: Set[HasParamFact] = set()
    revert_facts_dl: Set[RevertFact] = set() 
    require_facts_dl: Set[RequireFact] = set() 
    emit_facts_dl: Set[EmitFact] = set()

    ctmodifier_facts_dl: Set[CtModFact] =  set() 
    fnmodifier_facts_dl: Set[FnModFact] = set() 
    override_facts_dl: Set[OverrideFact] = set() 
    inherit_facts_dl: Set[InheritFact] = set() 
    callfact_facts_dl: Set[CallFact] = set() 
    statevar_facts_dl: Set[StateVarFact] = set()

    isContract_facts_dl: Set[IsContractFact] = set()
    isInterface_facts_dl: Set[IsInterfaceFact] = set()

    isImplemented_facts_dl: Set[IsImplementedFact] = set()


    for contract in slither.contracts:
        if contract.is_interface:
            isInterface_facts_dl.add(IsInterfaceFact(contract.name))
        else:
            isContract_facts_dl.add(IsContractFact(contract.name))

        # print(index, contract.name, len(contract.functions), len(contract.modifiers), len(contract.variables))
        hasStateVariables = processStateVariables(contract.name, contract.variables)
        all_hasParams = []
        all_hasRequire = []
        all_hasEvents = []
        all_hasIfEvents = []
        all_hasIfReverts = []
        all_hasIfNotReverts = []
        all_functioncalls = []
        all_useModifiers = []
        all_modifier_hasParams = []
        all_hasOverriden_funcs = []

        all_functioncalls_full = []
        
        for function in contract.functions:
                if function.is_implemented:
                    isImplemented_facts_dl.add(IsImplementedFact(contract.name, function.name))
            # if function.is_declared_by(contract) or len(function.functions_shadowed)>0:
                funcName = function.name
                params = function.parameters
                hasParams = processFunctionParameters(funcName, params)
                all_hasParams.extend(hasParams)
                hasRequire = processRequire(function=function)
                all_hasRequire.extend(hasRequire)
                hasIfReverts, hasIfNotReverts = processIFREVERTs(function=function)
                all_hasIfReverts.extend(hasIfReverts)
                all_hasIfNotReverts.extend(hasIfNotReverts)
                hasEvents, hasIfEvents = processEvents(function=function)
                all_hasEvents.extend(hasEvents)
                all_hasIfEvents.extend(hasIfEvents)
                hasFunctionCalls, hasFunctionCalls_full = processFunctionCall(function=function)
                all_functioncalls.extend(hasFunctionCalls)
                all_functioncalls_full.extend(hasFunctionCalls_full)
                useModifiers = processUseModifiers(function=function)
                all_useModifiers.extend(useModifiers)

        for function in contract.functions_declared:
                hasOverriden_funcs = processFunctionOverride(contract=contract, function=function)
                all_hasOverriden_funcs.extend(hasOverriden_funcs)

        for modifier in contract.modifiers:
                funcName = modifier.name
                params = modifier.parameters
                hasParams = processFunctionParameters(funcName, params)
                all_modifier_hasParams.extend(hasParams)
     
        for function in contract.functions:
            # if function.is_declared_by(contract) or len(function.functions_shadowed)>0:
                funcName = function.name
                params = function.parameters
                funcParam[f"{contract.name}.{funcName}"] = [ param.name for param in params] 

        with open(f"{factsdir}/{contract.name}.facts", "w") as f: 
        # with open(f"./library-facts/openzeppelin/{contract.name}.facts", "w") as f:
            for inherit_contract in contract.inheritance:
                parentName = inherit_contract.name
                f.write(f"CONTRACT,{contract.name},IS,{parentName}\n")
                inherit_facts_dl.add(InheritFact(parentName, contract.name))

            for function in contract.functions:
                f.write(f"CONTRACT,{contract.name},HASFUNCTION,{function.name}\n")
                hasFn_facts_dl.add(HasFnFact(contract.name, function.name))

            for function in contract.modifiers:
                f.write(f"CONTRACT,{contract.name},HASMODIFIER,{function.name}\n")
                ctmodifier_facts_dl.add(CtModFact(contract.name, function.name))

            for contractName, variable in hasStateVariables:
                f.write(f"CONTRACE,{contractName},HASSTATEVARIABLE,{variable}\n")
                statevar_facts_dl.add(StateVarFact(ct=contract.name, state_var=variable))

            for funcName, param in all_hasParams:
                f.write(f"FUNCTION,{contract.name}.{funcName},HASPARAM,{param}\n")
                hasParam_facts_dl.add(HasParamFact(contract.name, funcName, param))

            for funcName, param in all_modifier_hasParams:
                f.write(f"MODIFIER,{contract.name}.{funcName},HASPARAM,{param}\n")
                # TODO:  treat equally for functions and modifiers having parameters
                hasParam_facts_dl.add(HasParamFact(contract.name, funcName, param))

            for funcName, modifierName in all_useModifiers:
                f.write(f"FUNCTION,{contract.name}.{funcName},USEMODIFIER,{contract.name}.{modifierName}\n")
                fnmodifier_facts_dl.add(FnModFact(contract.name, funcName, modifierName))

            for item in all_hasOverriden_funcs:
                assert len(item[1:]) == 2
                f.write(f"FUNCTION,{contract.name}.{item[0]},OVERRIDE,{item[1]}.{item[2]}\n")
                override_facts_dl.add(OverrideFact(parent_ct=item[1], parent_fn=item[2], child_ct= contract.name, child_fn=item[0]))

            for req_item in all_hasRequire:
                funcName, conds = req_item[0], req_item[1:]
                f.write(f"FUNCTION,{contract.name}.{funcName},REQUIRE,"+",".join(conds)+"\n")
                require_facts_dl.add(RequireFact(contract.name, funcName, conds2Expr(conds)))

            for req_item in all_hasIfReverts:
                funcName, conds = req_item[0], req_item[1:]
                f.write(f"FUNCTION,{contract.name}.{funcName},REVERTIF,"+",".join(conds)+"\n")
                revert_facts_dl.add(RevertFact(contract.name, funcName, conds2Expr(conds)))

            for req_item in all_hasIfNotReverts:
                funcName, conds = req_item[0], req_item[1:]
                f.write(f"FUNCTION,{contract.name}.{funcName},REVERTIFNOT,"+",".join(conds)+"\n")
                notconds = ["NOT"]
                notconds.extend(conds)
                revert_facts_dl.add(RevertFact(contract.name, funcName, conds2Expr(notconds)))

            for funcName, event in all_hasEvents:
                f.write(f"FUNCTION,{contract.name}.{funcName},EMIT,{event}\n")
                emit_facts_dl.add(EmitFact(contract.name, funcName, event, Bool(True)))

            for funcName, event in all_hasIfEvents:
                f.write(f"FUNCTION,{contract.name}.{funcName},EMITIF,{event}\n")
                # TODO: code fact: might emit a event
                emit_facts_dl.add(EmitFact(contract.name, funcName, event, Expr("")))

            for item in all_functioncalls:
                if len(item[1:]) == 1:
                    f.write(f"FUNCTION,{contract.name}.{item[0]},CALL,{contract.name}.{item[1]}\n")
                else:
                    assert len(item[1:]) == 2
                    f.write(f"FUNCTION,{contract.name}.{item[0]},CALL,{item[1]}.{item[2]}\n")


            for item in all_functioncalls_full:
                if len(item) == 5:
                    fnName, arguments, callee_contract, calleefn_name, calleeFn_params = item  
                    dl_arguments = [ Expr(str(arg)) for arg in arguments]
                    dl_params = [ Param(str(param)) for param in calleeFn_params]
                    callfact_facts_dl.add(CallFact(ct_caller=contract.name, caller=fnName, actual_args=SouffleList(dl_arguments), ct_callee=callee_contract, callee=calleefn_name, params=SouffleList(dl_params)))
                else:
                    # call to other functions inside the same contract
                    assert len(item) == 4, "invalid call facts tuple: "+ item 
                    fnName, arguments, calleefn_name, calleeFn_params = item  
                    callee_contract = contract.name 
                    dl_arguments = [ Expr(str(arg)) for arg in arguments]
                    dl_params = [ Param(str(param)) for param in calleeFn_params]
                    callfact_facts_dl.add(CallFact(ct_caller=contract.name, caller=fnName, actual_args=SouffleList(dl_arguments), ct_callee=callee_contract, callee=calleefn_name, params=SouffleList(dl_params)))
               


        index += 1
    # print(len(slither.contracts))
    # parentdir =  os.path.dirname(os.path.abspath(factsdir))
    # dirname = os.path.basename(os.path.abspath(factsdir))
    with open(f"{factsdir}/contracts.json", "w") as f:
    # with open(f"./library-facts/openzeppelin.json", "w") as f:
        json.dump(funcParam, f)

    buildTransitive(factsdir=factsdir)


    dlfileOut = {
        "HasFn.facts": hasFn_facts_dl,
        "Require.facts": require_facts_dl,
        "Emit.facts": emit_facts_dl, 
        "Revert.facts": revert_facts_dl,
        "HasParam.facts": hasParam_facts_dl, 
        "CtHasMod.facts" : ctmodifier_facts_dl,
        "FnHasMod.facts" : fnmodifier_facts_dl,
        "Override.facts" : override_facts_dl,
        "Inherit.facts" : inherit_facts_dl,
        "Call.facts" : callfact_facts_dl,
        "StateVar.facts": statevar_facts_dl,
        "IsContract.facts": isContract_facts_dl,
        "IsInterface.facts": isInterface_facts_dl,
        "IsImplemented.facts": isImplemented_facts_dl
    }
    codefacts = "codefacts"
    if not os.path.exists(os.path.join(factsdir, codefacts)):
        os.mkdir(os.path.join(factsdir, codefacts))
    
    for fact_file in dlfileOut:
        with open(os.path.join(factsdir, codefacts, fact_file), 'w') as dl_f:
            dl_f.writelines([str(x) + os.linesep for x in dlfileOut[fact_file]])

