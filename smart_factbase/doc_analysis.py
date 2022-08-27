import json
import os
import subprocess as sub
from pathlib import Path
from typing import Set

from dapphub import extractDocFactsFromOneFunc_DappHub
from datalog.pred import SeeFnFact, HasFnFact, RequireFact, HasParamFact, CtModFact, \
    RevertFact, EmitFact, FnModFact, OverrideFact, InheritFact, StateVarFact, CallFact
from erc721_extensions import extractContractContainFacts_ERC721
from erc721_extensions import extractDocFactsFromOneFunc_ERC721
from macros import DOC_FACTS_OUTPUT_DIR
from macros import ERC721_REPO_DIR
from macros import OPEN_ZEPPELIN_REPO_DIR
from openzeppelin import copyOtherFactsToTheirOwnerFiles
from openzeppelin import extractContractContainFacts_OpenZeppelin
from openzeppelin import extractDocFactsFromOneFunc_OpenZeppelin


def extractDocFactsFromOneSrcFile(lib, version, src_file):
    if lib == 'openzeppelin':
        extractDocFactsFromOneSrcFile_OpenZeppelin(lib, version, src_file)
    elif lib.startswith('dapphub/'):
        extractDocFactsFromOneReadmeFile_DappHub(lib, version, src_file)
    elif lib == 'erc721-extensions':
        extractDocFactsFromOneSrcFile_ERC721(lib, version, src_file)


def extractDocFactsFromOneSrcFile_OpenZeppelin(lib, version, src_file):
    print('=== Extracting ' + src_file)
    cwd = os.getcwd()
    os.chdir(OPEN_ZEPPELIN_REPO_DIR)
    sub.run('git checkout ' + version, shell=True)
    os.chdir(cwd)
    output_dir: Path = Path(DOC_FACTS_OUTPUT_DIR) / lib / version
    contract_fqn = src_file.split('/')[-1].split('.')[0]
    output_json_file = output_dir / f"{contract_fqn}.json"
    dl_facts_dir = output_dir / "docfacts"
    if not dl_facts_dir.is_dir():
        os.makedirs(dl_facts_dir)
    doc_facts = []
    dl_see_fn: Set[SeeFnFact] = set()
    dl_require: Set[RequireFact] = set()
    dl_emit: Set[EmitFact] = set()
    dl_revert: Set[RevertFact] = set()
    dl_has_param: Set[HasParamFact] = set()
    dl_fn_mod: Set[FnModFact] = set()
    dl_call: Set[CallFact] = set()
    # contract-level
    doc_facts, dl_has_fn, dl_state_var, dl_ct_mod = extractContractContainFacts_OpenZeppelin(lib,
                                                                                             version,
                                                                                             src_file,
                                                                                             doc_facts,
                                                                                             contract_fqn)
    with open(src_file, 'r') as fr:
        lines = fr.readlines()
    for i in range(len(lines)):
        if lines[i].strip().startswith('/**'):
            start_idx = i
        if lines[i].strip() == '*/':
            end_idx = i
            j = i + 1
            while lines[j].strip().startswith('//'):
                j += 1
            if lines[j].strip().startswith('function '):
                func_name = lines[j].strip().split('function ')[-1].split('(')[0]
                doc_lines = lines[start_idx: end_idx + 1]
                # func-level
                doc_facts, see_fn_facts, require_facts, emit_facts, \
                revert_facts, has_param_facts, use_mod_facts, call_facts = extractDocFactsFromOneFunc_OpenZeppelin(
                    lib, version, doc_lines, contract_fqn, func_name, doc_facts)
                dl_see_fn = dl_see_fn.union(see_fn_facts)
                dl_require = dl_require.union(require_facts)
                dl_emit = dl_emit.union(emit_facts)
                dl_revert = dl_revert.union(revert_facts)
                dl_has_param = dl_has_param.union(has_param_facts)
                dl_fn_mod = dl_fn_mod.union(use_mod_facts)
                dl_call = dl_call.union(call_facts)
            else:
                # we do not analyze struct doc for now
                pass
    for fact in doc_facts:
        print(fact)
    copyOtherFactsToTheirOwnerFiles(lib, version, doc_facts, contract_fqn)
    with open(output_json_file, 'w') as fw:
        json.dump(doc_facts, fw, indent=2)
    write_dl_facts(dl_facts_dir, dl_has_fn, dl_see_fn, dl_require, dl_emit,
                   dl_revert, dl_has_param, dl_fn_mod, set(), set(), dl_state_var, dl_call, dl_ct_mod)


def write_dl_facts(fact_dir: Path, has_fn_facts: Set[HasFnFact], see_fn_facts: Set[SeeFnFact],
                   require_facts: Set[RequireFact], emit_facts: Set[EmitFact],
                   revert_facts: Set[RevertFact], has_param_facts: Set[HasParamFact],
                   fn_mod_facts: Set[FnModFact], override_facts: Set[OverrideFact],
                   inherit_facts: Set[InheritFact], state_var_facts: Set[StateVarFact],
                   call_facts: Set[CallFact], ct_mod_facts: Set[CtModFact]):
    with open(fact_dir / "SeeFn.facts", 'a') as dl_f:
        dl_f.writelines([str(x) + os.linesep for x in see_fn_facts])
    with open(fact_dir / "HasFn.facts", 'a') as dl_f:
        dl_f.writelines([str(x) + os.linesep for x in has_fn_facts])
    with open(fact_dir / "Require.facts", 'a') as dl_f:
        dl_f.writelines([str(x) + os.linesep for x in require_facts])
    with open(fact_dir / "Emit.facts", 'a') as dl_f:
        dl_f.writelines([str(x) + os.linesep for x in emit_facts])
    with open(fact_dir / "Revert.facts", 'a') as dl_f:
        dl_f.writelines([str(x) + os.linesep for x in revert_facts])
    with open(fact_dir / "HasParam.facts", 'a') as dl_f:
        dl_f.writelines([str(x) + os.linesep for x in has_param_facts])
    with open(fact_dir / "FnHasMod.facts", 'a') as dl_f:
        dl_f.writelines([str(x) + os.linesep for x in fn_mod_facts])
    with open(fact_dir / "Override.facts", 'a') as dl_f:
        dl_f.writelines([str(x) + os.linesep for x in override_facts])
    with open(fact_dir / "Inherit.facts", 'a') as dl_f:
        dl_f.writelines([str(x) + os.linesep for x in inherit_facts])
    with open(fact_dir / "HasStateVar.facts", 'a') as dl_f:
        dl_f.writelines([str(x) + os.linesep for x in state_var_facts])
    with open(fact_dir / "Call.facts", 'a') as dl_f:
        dl_f.writelines([str(x) + os.linesep for x in call_facts])
    with open(fact_dir / "CtHasMod.facts", 'a') as dl_f:
        dl_f.writelines([str(x) + os.linesep for x in ct_mod_facts])


def extractDocFactsFromOneSrcFile_ERC721(lib, version, src_file):
    print('=== Extracting ' + src_file)
    cwd = os.getcwd()
    os.chdir(ERC721_REPO_DIR)
    sub.run('git checkout ' + version, shell=True)
    os.chdir(cwd)
    output_dir: Path = Path(DOC_FACTS_OUTPUT_DIR) / lib / version
    contract_fqn = src_file.split('/')[-1].split('.')[0]
    output_json_file = output_dir / f"{contract_fqn}.json"
    dl_facts_dir = output_dir / "docfacts"
    if not dl_facts_dir.is_dir():
        os.makedirs(dl_facts_dir)
    doc_facts = []
    # contract-level
    doc_facts, dl_has_fn = extractContractContainFacts_ERC721(lib, version, src_file, doc_facts)
    with open(src_file, 'r') as fr:
        lines = fr.readlines()
    start_idx = -1
    dl_fn_mod: Set[FnModFact] = set()
    dl_require: Set[RequireFact] = set()
    dl_emit: Set[EmitFact] = set()
    dl_revert: Set[RevertFact] = set()
    dl_has_param: Set[HasParamFact] = set()
    dl_override: Set[OverrideFact] = set()
    dl_inherit: Set[InheritFact] = set()
    for i in range(len(lines)):
        if lines[i].strip().startswith('///') and start_idx == -1:
            start_idx = i
        if lines[i].strip().startswith('///') and not lines[i + 1].strip().startswith('///'):
            end_idx = i
            j = i + 1
            while lines[j].strip().startswith('//'):
                j += 1
            if lines[j].strip().startswith('function '):
                func_name = lines[j].strip().split('function ')[-1].split('(')[0]
                doc_lines = lines[start_idx: end_idx + 1]
                # func-level
                doc_facts, fn_mod_facts, require_facts, emit_facts, revert_facts, \
                has_param_facts, override_facts, inherit_facts = \
                    extractDocFactsFromOneFunc_ERC721(lib, version, doc_lines, contract_fqn,
                                                      func_name, doc_facts)
                dl_fn_mod = dl_fn_mod.union(fn_mod_facts)
                dl_require = dl_require.union(require_facts)
                dl_emit = dl_emit.union(emit_facts)
                dl_revert = dl_revert.union(revert_facts)
                dl_has_param = dl_has_param.union(has_param_facts)
                dl_override = dl_override.union(override_facts)
                dl_inherit = dl_inherit.union(inherit_facts)
            elif lines[j].strip().startswith('modifier '):
                pass
            elif lines[j].strip().startswith('constructor '):
                pass
            else:
                # we do not analyze struct doc for now
                pass
            start_idx = -1
    for fact in doc_facts:
        print(fact)
    copyOtherFactsToTheirOwnerFiles(lib, version, doc_facts, contract_fqn)
    write_dl_facts(dl_facts_dir, dl_has_fn, set(), dl_require, dl_emit,
                   dl_revert, dl_has_param, dl_fn_mod, dl_override, dl_inherit, set(), set(), set())
    with open(output_json_file, 'w') as fw:
        json.dump(doc_facts, fw, indent=2)


def extractDocFactsFromOneReadmeFile_DappHub(lib, version, src_file):
    print('=== Extracting ' + src_file)
    output_dir: Path = Path(DOC_FACTS_OUTPUT_DIR) / lib
    dl_facts_dir = output_dir / "docfacts"
    if not dl_facts_dir.is_dir():
        os.makedirs(dl_facts_dir)

    with open(src_file, 'r') as fr:
        lines = fr.readlines()
    start_idx = -1

    dl_has_fn: Set[HasFnFact] = set()
    dl_require: Set[RequireFact] = set()
    dl_emit: Set[EmitFact] = set()
    dl_override: Set[OverrideFact] = set()
    dl_fn_mod: Set[FnModFact] = set()
    for i in range(len(lines)):
        if lines[i].strip().startswith('<h2>'):
            contract_fqn = lines[i].strip().split('<h2>')[-1]
            start_idx = -1
            output_json_file = output_dir / f"{contract_fqn}.json"
            doc_facts = []
            # contract-level
        if lines[i].strip().startswith('#### `'):
            start_idx = i + 1
        if start_idx != -1 and lines[i].strip() == '':
            end_idx = i
            func_name = lines[start_idx - 1].strip().split('`')[1].split('(')[0]
            contract_fact = 'CONTRACT,' + contract_fqn + ',HASFUNCTION,' + func_name
            if contract_fact not in doc_facts:
                doc_facts.append(contract_fact)
            dl_has_fn.add(HasFnFact(contract_fqn, func_name))
            doc_lines = lines[start_idx: end_idx]
            doc_facts, require_facts, emit_facts, override_facts, fn_mod_facts = extractDocFactsFromOneFunc_DappHub(
                lib, version, doc_lines, contract_fqn, func_name, doc_facts)
            dl_require = dl_require.union(require_facts)
            dl_emit = dl_emit.union(emit_facts)
            dl_override = dl_override.union(override_facts)
            dl_fn_mod = dl_fn_mod.union(fn_mod_facts)
            with open(output_json_file, 'w') as fw:
                json.dump(doc_facts, fw, indent=2)

    write_dl_facts(dl_facts_dir, dl_has_fn, set(), dl_require, dl_emit, set(), set(), dl_fn_mod,
                   dl_override, set(), set(), set(), set())
