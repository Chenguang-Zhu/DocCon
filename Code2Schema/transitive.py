from calendar import c
import os
import argparse
import  json 
from toposort import toposort, toposort_flatten

REQUIRE = "REQUIRE"
EMIT = "EMIT"
EMITIF = "EMITIF"
IS = "IS" # IS may not be useful
FUNCTIONCALL = "CALL"
HASFUNCTION = "HASFUNCTION"
HASMODIFIER = "HASMODIFIER"
USEMODIFIER = "USEMODIFIER"
HASSTATEVARIABLE = "HASSTATEVARIABLE"
REVERTIF = "REVERTIF"
REVERTIFNOT = "REVERTIFNOT"
HASPARAM = "HASPARAM"
OVERRIDE = "OVERRIDE"

TYPE_CONTRACT = "CONTRACT"
TYPE_FUNCTION = "FUNCTION"
TYPE_MODIFIER = "MODIFIER"

REQUIRE_FACTS = dict()
EMIT_FACTS = dict()
EMITIF_FACTS = dict()
IS_FACTS = dict()
FUNCTIONCALL_FACTS = dict()
HASFUNCTION_FACTS = dict()
HASMODIFIER_FACTS = dict()
USEMODIFIER_FACTS = dict()
HASSTATEVARIABLE_FACTS = dict()
REVERTIF_FACTS = dict()
REVERTIFNOT_FACTS = dict()
HASPARAM_FACTS = dict()
MODIFIERHASPARAM_FACTS = dict()
OVERRIDENFUNCS_FACTS = dict()

# 
def processFact(fact):
    fact = fact.strip()
    items = fact.split(",")
    try:
        TYPE_KEYWORD = items[0]
        SCHEMA_KEYWORD = items[2]
    except:
        print(fact)
        raise Exception("parsing error")
    if SCHEMA_KEYWORD  ==  IS:
            contract = items[1]
            parentContract = items[3]
            if contract not in IS_FACTS:
                IS_FACTS[contract] = list()
            IS_FACTS[contract].append(parentContract)
    elif SCHEMA_KEYWORD == HASSTATEVARIABLE:
            contract = items[1]
            statevar = items[3]
            if contract not in HASSTATEVARIABLE_FACTS:
                HASSTATEVARIABLE_FACTS[contract] = set() 
            HASSTATEVARIABLE_FACTS[contract].add(statevar)
    elif SCHEMA_KEYWORD ==  HASFUNCTION:
            contract = items[1]
            function = items[3]
            if contract not in HASFUNCTION_FACTS:
                HASFUNCTION_FACTS[contract] = set()
            HASFUNCTION_FACTS[contract].add(function)
    elif SCHEMA_KEYWORD == HASMODIFIER:
            contract = items[1]
            function = items[3]
            if contract not in HASMODIFIER_FACTS:
                HASMODIFIER_FACTS[contract] = set() 
            HASMODIFIER_FACTS[contract].add(function)
    elif TYPE_KEYWORD == TYPE_FUNCTION and  SCHEMA_KEYWORD == HASPARAM:
            function = items[1]
            param = items[3]
            if function not in HASPARAM_FACTS:
                HASPARAM_FACTS[function] = set()
            HASPARAM_FACTS[function].add(param)
    elif TYPE_KEYWORD == TYPE_MODIFIER and SCHEMA_KEYWORD == HASPARAM:
            modifer = items[1]
            param = items[3]
            if modifer not in MODIFIERHASPARAM_FACTS:
                MODIFIERHASPARAM_FACTS[modifer] = set()
            MODIFIERHASPARAM_FACTS[modifer].add(param)
    elif SCHEMA_KEYWORD == OVERRIDE:
            function = items[1]
            callee = items[3]
            if function not in OVERRIDENFUNCS_FACTS:
                OVERRIDENFUNCS_FACTS[function] = set()
            OVERRIDENFUNCS_FACTS[function].add(callee)
    elif SCHEMA_KEYWORD == FUNCTIONCALL:
            function = items[1]
            callee = items[3]
            if function not in FUNCTIONCALL_FACTS:
                FUNCTIONCALL_FACTS[function] = set()
            FUNCTIONCALL_FACTS[function].add(callee)
    elif SCHEMA_KEYWORD == USEMODIFIER:
            function = items[1]
            callee = items[3]
            if function not in USEMODIFIER_FACTS:
                USEMODIFIER_FACTS[function] = set()
            USEMODIFIER_FACTS[function].add(callee)
    elif SCHEMA_KEYWORD ==  REQUIRE or SCHEMA_KEYWORD ==  EMIT \
        or SCHEMA_KEYWORD == EMITIF or SCHEMA_KEYWORD == REVERTIF or SCHEMA_KEYWORD == REVERTIFNOT:
        function = items[1]
        if SCHEMA_KEYWORD == REQUIRE:
            if function not in REQUIRE_FACTS:
                REQUIRE_FACTS[function] = set()
            REQUIRE_FACTS[function].add(fact)
        elif SCHEMA_KEYWORD == EMIT:
            if function not in EMIT_FACTS:
                EMIT_FACTS[function] = set()
            EMIT_FACTS[function].add(fact)
        elif SCHEMA_KEYWORD == EMITIF:
            if function not in EMITIF_FACTS:
                EMITIF_FACTS[function] = set()
            EMITIF_FACTS[function].add(fact)
        elif SCHEMA_KEYWORD ==  REVERTIF:
            if function not in REVERTIF_FACTS:
                REVERTIF_FACTS[function] = set()
            REVERTIF_FACTS[function].add(fact)
        elif SCHEMA_KEYWORD == REVERTIFNOT:
            if function not in REVERTIFNOT_FACTS:
                REVERTIFNOT_FACTS[function] = set()
            REVERTIFNOT_FACTS[function].add(fact)
        else:
            assert False

def processSingleContractFacts(factsfile):
    contractName = os.path.basename(factsfile)
    with open(factsfile, "r") as f:
        facts = f.readlines()
        for fact in facts:
            processFact(fact)
    return contractName 

def getRequireFixPoint(contractName, function, visited :set):
    if f"{contractName}.{function}" not in REQUIRE_FACTS:
        REQUIRE_FACTS[f"{contractName}.{function}"] = set()
    if f"{contractName}.{function}" in visited:
        return REQUIRE_FACTS[f"{contractName}.{function}"]
    visited.add(f"{contractName}.{function}")
    requirefacts = set()
    if f"{contractName}.{function}" in FUNCTIONCALL_FACTS:
        for callee in FUNCTIONCALL_FACTS[f"{contractName}.{function}"]:
            try:
                _contractName, _function = callee.split(".")
            except:
                print(callee)
                exit(0)
            _facts = getRequireFixPoint(contractName=_contractName, function=_function, visited=visited)
            for fact in _facts:
                requirefacts.add(fact.replace(f"{_contractName}.{_function}", f"{contractName}.{function}"))
    if f"{contractName}.{function}" in USEMODIFIER_FACTS:
        for callee in USEMODIFIER_FACTS[f"{contractName}.{function}"]:
            try:
                _contractName, _function = callee.split(".")
            except:
                # print(callee)
                _contractName, _function = contractName, callee.strip()
            _facts = getRequireFixPoint(contractName=_contractName, function=_function, visited=visited)
            for fact in _facts:
                requirefacts.add(fact.replace(f"{_contractName}.{_function}", f"{contractName}.{function}"))
    REQUIRE_FACTS[f"{contractName}.{function}"].update(requirefacts)
    return REQUIRE_FACTS[f"{contractName}.{function}"]

def getEmitFixPoint(contractName, function, visited :set):
    if f"{contractName}.{function}" not in EMIT_FACTS:
        EMIT_FACTS[f"{contractName}.{function}"] = set()
    if f"{contractName}.{function}" in visited:
        return EMIT_FACTS[f"{contractName}.{function}"]
    requirefacts = set()
    visited.add(f"{contractName}.{function}")
    if f"{contractName}.{function}" in FUNCTIONCALL_FACTS:
        for callee in FUNCTIONCALL_FACTS[f"{contractName}.{function}"]:
            _contractName, _function = callee.split(".")
            _facts = getEmitFixPoint(contractName=_contractName, function=_function, visited=visited)
            for fact in _facts:
                requirefacts.add(fact.replace(f"{_contractName}.{_function}", f"{contractName}.{function}"))
    if f"{contractName}.{function}" in USEMODIFIER_FACTS:
        for callee in USEMODIFIER_FACTS[f"{contractName}.{function}"]:
            try:
                _contractName, _function = callee.split(".")
            except:
                # print(callee)
                _contractName, _function = contractName, callee.strip()
            _facts = getEmitFixPoint(contractName=_contractName, function=_function, visited=visited)
            for fact in _facts:
                requirefacts.add(fact.replace(f"{_contractName}.{_function}", f"{contractName}.{function}"))
    EMIT_FACTS[f"{contractName}.{function}"].update(requirefacts)
    return EMIT_FACTS[f"{contractName}.{function}"]

def getEmitIfFixPoint(contractName, function, visited :set):
    if f"{contractName}.{function}" not in EMITIF_FACTS:
        EMITIF_FACTS[f"{contractName}.{function}"] = set()
    if f"{contractName}.{function}" in visited:
        return EMITIF_FACTS[f"{contractName}.{function}"]
    requirefacts = set()
    visited.add(f"{contractName}.{function}")
    if f"{contractName}.{function}" in FUNCTIONCALL_FACTS:
        for callee in FUNCTIONCALL_FACTS[f"{contractName}.{function}"]:
            _contractName, _function = callee.split(".")
            _facts = getEmitIfFixPoint(contractName=_contractName, function=_function, visited=visited)
            for fact in _facts:
                requirefacts.add(fact.replace(f"{_contractName}.{_function}", f"{contractName}.{function}"))
    if f"{contractName}.{function}" in USEMODIFIER_FACTS:
        for callee in USEMODIFIER_FACTS[f"{contractName}.{function}"]:
            try:
                _contractName, _function = callee.split(".")
            except:
                # print(callee)
                _contractName, _function = contractName, callee.strip()
            _facts = getEmitIfFixPoint(contractName=_contractName, function=_function, visited=visited)
            for fact in _facts:
                requirefacts.add(fact.replace(f"{_contractName}.{_function}", f"{contractName}.{function}"))
    EMITIF_FACTS[f"{contractName}.{function}"].update(requirefacts)
    return EMITIF_FACTS[f"{contractName}.{function}"]

def getReverIfFixPoint(contractName, function, visited :set):
    if f"{contractName}.{function}" not in REVERTIF_FACTS:
        REVERTIF_FACTS[f"{contractName}.{function}"] = set()
    if f"{contractName}.{function}" in visited:
        return REVERTIF_FACTS[f"{contractName}.{function}"]
    requirefacts = set()
    visited.add(f"{contractName}.{function}")
    if f"{contractName}.{function}" in FUNCTIONCALL_FACTS:
        for callee in FUNCTIONCALL_FACTS[f"{contractName}.{function}"]:
            _contractName, _function = callee.split(".")
            _facts = getReverIfFixPoint(contractName=_contractName, function=_function, visited=visited)
            for fact in _facts:
                requirefacts.add(fact.replace(f"{_contractName}.{_function}", f"{contractName}.{function}"))
    if f"{contractName}.{function}" in USEMODIFIER_FACTS:
        for callee in USEMODIFIER_FACTS[f"{contractName}.{function}"]:
            try:
                _contractName, _function = callee.split(".")
            except:
                # print(callee)
                _contractName, _function = contractName, callee.strip()
            _facts = getReverIfFixPoint(contractName=_contractName, function=_function, visited=visited)
            for fact in _facts:
                requirefacts.add(fact.replace(f"{_contractName}.{_function}", f"{contractName}.{function}"))
    REVERTIF_FACTS[f"{contractName}.{function}"].update(requirefacts)
    return REVERTIF_FACTS[f"{contractName}.{function}"]

def getReverIfNotFixPoint(contractName, function, visited :set):
    if f"{contractName}.{function}" not in REVERTIFNOT_FACTS:
        REVERTIFNOT_FACTS[f"{contractName}.{function}"] = set()
    if f"{contractName}.{function}" in visited:
        return REVERTIFNOT_FACTS[f"{contractName}.{function}"]
    requirefacts = set()
    visited.add(f"{contractName}.{function}")
    if f"{contractName}.{function}" in FUNCTIONCALL_FACTS:
        for callee in FUNCTIONCALL_FACTS[f"{contractName}.{function}"]:
            _contractName, _function = callee.split(".")
            _facts = getReverIfNotFixPoint(contractName=_contractName, function=_function, visited=visited)
            for fact in _facts:
                requirefacts.add(fact.replace(f"{_contractName}.{_function}", f"{contractName}.{function}"))
    if f"{contractName}.{function}" in USEMODIFIER_FACTS:
        for callee in USEMODIFIER_FACTS[f"{contractName}.{function}"]:
            try:
                _contractName, _function = callee.split(".")
            except:
                # print(callee)
                _contractName, _function = contractName, callee.strip()
            _facts = getReverIfNotFixPoint(contractName=_contractName, function=_function, visited=visited)
            for fact in _facts:
                requirefacts.add(fact.replace(f"{_contractName}.{_function}", f"{contractName}.{function}"))
    REVERTIFNOT_FACTS[f"{contractName}.{function}"].update(requirefacts)
    return REVERTIFNOT_FACTS[f"{contractName}.{function}"]

def buildTransitive(factsdir):
    contracts = set()
    for item in os.listdir(factsdir):
        file = os.path.join(factsdir,item)
        if file.endswith(".facts"):
            contractName = processSingleContractFacts(factsfile=file)
            contractName = contractName.split(".")[0]
            # we assert there is no two contracts with the same name 
            assert contractName not in contracts  
            contracts.add(contractName)
    
    visited_1 = set()
    visited_2 = set()
    visited_3 = set()
    visited_4 = set()
    visited_5 = set()
    for contractName in contracts:
        if contractName in HASFUNCTION_FACTS:
            for function in HASFUNCTION_FACTS[contractName]:
                REQUIRE_FACTS[f"{contractName}.{function}"] =  getRequireFixPoint(contractName, function, visited_1)
                EMIT_FACTS[f"{contractName}.{function}"] = getEmitFixPoint(contractName=contractName, function=function, visited=visited_2)
                EMITIF_FACTS[f"{contractName}.{function}"] = getEmitIfFixPoint(contractName=contractName, function=function, visited=visited_3)
                REVERTIF_FACTS[f"{contractName}.{function}"] =  getReverIfFixPoint(contractName=contractName, function=function, visited=visited_4)
                REVERTIFNOT_FACTS[f"{contractName}.{function}"] = getReverIfNotFixPoint(contractName=contractName, function=function, visited=visited_5)
    # tmp = "./tmp"
    # if not os.path.exists(tmp):
    #     os.makedirs(tmp)
    # write back facts with transitive extension
    for contractName in contracts:
        if contractName not in IS_FACTS:
            IS_FACTS[contractName] = list()
        factscontract = os.path.join(factsdir, contractName+".facts") 
        with open(factscontract, "w") as f:
            if contractName in IS_FACTS:
                for parent in IS_FACTS[contractName]:
                        fact = f"CONTRACT,{contractName},IS,{parent}\n"
                        f.write(fact)
            if contractName in HASSTATEVARIABLE_FACTS:
                for statevar in HASSTATEVARIABLE_FACTS[contractName]:
                        fact = f"CONTRACT,{contractName},HASSTATEVARIABLE,{statevar}\n"
                        f.write(fact)
            if contractName in HASMODIFIER_FACTS:
                for function in HASMODIFIER_FACTS[contractName]:
                        fact = f"CONTRACT,{contractName},HASMODIFIER,{function}\n"
                        f.write(fact)
                        if f"{contractName}.{function}" in REQUIRE_FACTS:
                            if len(REQUIRE_FACTS[f"{contractName}.{function}"])>0:
                                f.write("\n".join(REQUIRE_FACTS[f"{contractName}.{function}"]))
                                f.write("\n")
                        if f"{contractName}.{function}" in EMIT_FACTS:
                            if len(EMIT_FACTS[f"{contractName}.{function}"])>0:
                                f.write("\n".join(EMIT_FACTS[f"{contractName}.{function}"]))
                                f.write("\n")
                        if f"{contractName}.{function}" in EMITIF_FACTS:
                            if len(EMITIF_FACTS[f"{contractName}.{function}"])>0:
                                f.write("\n".join(EMITIF_FACTS[f"{contractName}.{function}"]))
                                f.write("\n")
                        if f"{contractName}.{function}" in REVERTIF_FACTS:
                            if len(REVERTIF_FACTS[f"{contractName}.{function}"])>0:
                                f.write("\n".join(REVERTIF_FACTS[f"{contractName}.{function}"]))
                                f.write("\n")
                        if f"{contractName}.{function}" in REVERTIFNOT_FACTS:
                            if len(REVERTIFNOT_FACTS[f"{contractName}.{function}"])>0:
                                f.write("\n".join(REVERTIFNOT_FACTS[f"{contractName}.{function}"]))
                                f.write("\n")
                        if f"{contractName}.{function}" in MODIFIERHASPARAM_FACTS:
                            for param in MODIFIERHASPARAM_FACTS[f"{contractName}.{function}"]:
                                    fact = f"MODIFIER,{contractName}.{function},HASPARAM,{param}\n"
                                    f.write(fact)
           
            if contractName in HASFUNCTION_FACTS:
                for function in HASFUNCTION_FACTS[contractName]:
                        fact = f"CONTRACT,{contractName},HASFUNCTION,{function}\n"
                        f.write(fact)
                        if f"{contractName}.{function}" in HASPARAM_FACTS:
                            for param in HASPARAM_FACTS[f"{contractName}.{function}"]:
                                fact = f"FUNCTION,{contractName}.{function},HASPARAM,{param}\n"
                                f.write(fact)
                        if f"{contractName}.{function}" in USEMODIFIER_FACTS:
                            for callee in USEMODIFIER_FACTS[f"{contractName}.{function}"]:
                                if callee.find(".")==-1:
                                    callee = f"{contractName}.{callee}"
                                fact = f"FUNCTION,{contractName}.{function},USEMODIFIER,{callee}\n"
                                f.write(fact)    
                        if f"{contractName}.{function}" in OVERRIDENFUNCS_FACTS:
                            for overriden_func in OVERRIDENFUNCS_FACTS[f"{contractName}.{function}"]:
                                    fact = f"FUNCTION,{contractName}.{function},OVERRIDE,{overriden_func}\n"
                                    f.write(fact)
                        if f"{contractName}.{function}" in FUNCTIONCALL_FACTS:
                            for callee in FUNCTIONCALL_FACTS[f"{contractName}.{function}"]:
                                if callee.find(".")==-1:
                                    callee = f"{contractName}.{callee}"
                                fact = f"FUNCTION,{contractName}.{function},CALL,{callee}\n"
                                f.write(fact)
                        if f"{contractName}.{function}" in REQUIRE_FACTS:
                            if len(REQUIRE_FACTS[f"{contractName}.{function}"])>0:
                                f.write("\n".join(REQUIRE_FACTS[f"{contractName}.{function}"]))
                                f.write("\n")
                        if f"{contractName}.{function}" in EMIT_FACTS:
                            if len(EMIT_FACTS[f"{contractName}.{function}"])>0:
                                f.write("\n".join(EMIT_FACTS[f"{contractName}.{function}"]))
                                f.write("\n")
                        if f"{contractName}.{function}" in EMITIF_FACTS:
                            if len(EMITIF_FACTS[f"{contractName}.{function}"])>0:
                                f.write("\n".join(EMITIF_FACTS[f"{contractName}.{function}"]))
                                f.write("\n")
                        if f"{contractName}.{function}" in REVERTIF_FACTS:
                            if len(REVERTIF_FACTS[f"{contractName}.{function}"])>0:
                                f.write("\n".join(REVERTIF_FACTS[f"{contractName}.{function}"]))
                                f.write("\n")
                        if f"{contractName}.{function}" in REVERTIFNOT_FACTS:
                            if len(REVERTIFNOT_FACTS[f"{contractName}.{function}"])>0:
                                f.write("\n".join(REVERTIFNOT_FACTS[f"{contractName}.{function}"]))
                                f.write("\n")
    inheritances = os.path.join(factsdir, "inheritance.json") 
    with open(inheritances, "w") as f:
        json.dump(IS_FACTS, f)
    
    inheritances_topsort = os.path.join(factsdir, "inheritance_toposort.json") 
    with open(inheritances_topsort, "w") as f:
        inh_sorted = list(toposort_flatten(IS_FACTS))
        inh_sorted = [ item for item in inh_sorted if item.find("Mock")==-1]
        # print(inh_sorted)
        json.dump(inh_sorted, f)

def test():
    # factsfile = "../library-facts/openzeppelin/release-v4.5/AccessControl.facts"
    # processSingleContractFacts(factsfile=factsfile)
    # print(IS_FACTS)
    # print(HASFUNCTION_FACTS)
    # print(HASMODIFIER_FACTS)
    # print(REQUIRE_FACTS)
    # print(REVERTIF_FACTS)
    # print(HASPARAM_FACTS)
    usage = "python3 transitive.py factsdir \n"
    usage += "\t the extended facts will be written back to the same facts directory\n"
    parser = argparse.ArgumentParser(
        description="Extend facts with transitive relation",
        usage=usage,
    )
    parser.add_argument("factsdir", help=argparse.SUPPRESS)
    args = parser.parse_args()
    factsdir = args.factsdir
    # factsdir = "../library-facts/openzeppelin/release-v4.5/"
    buildTransitive(factsdir=factsdir)
    # target = "Governor.castVoteBySig"
    # print(EMIT_FACTS[target])
    # target = "Governor"
    # print(target, IS_FACTS[target])
    

if __name__=="__main__":
    test()