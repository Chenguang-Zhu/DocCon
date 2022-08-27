import argparse
import sys

from doc_analysis import extractDocFactsFromOneSrcFile
from query import checkContractCodeDocInconsistency
from query import checkFuncCodeDocInconsistency


def parseArgs(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--extract-doc', help='Extract doc facts', required=False)
    parser.add_argument('--check', help='Check code-doc inconsistency', action='store_true', required=False)
    parser.add_argument('--contract', help='contract name', required=False)
    parser.add_argument('--func', help='function name', required=False)
    parser.add_argument('--level', help='alert level', required=False)
    parser.add_argument('--lib', help='library', required=False)
    parser.add_argument('--version', help='the library version', required=False)
    if len(argv) == 0:
        parser.print_help()
        exit(1)
    opts = parser.parse_args(argv)
    return opts

if __name__ == '__main__':
    opts = parseArgs(sys.argv[1:])
    if opts.extract_doc:
        src_file = opts.extract_doc
        lib = opts.lib
        version = opts.version
        extractDocFactsFromOneSrcFile(lib, version, src_file)
        exit(0)
    if opts.check:
        contract_name = opts.contract
        func_name = opts.func
        level = opts.level
        lib = opts.lib
        version = opts.version
        if func_name:
            checkFuncCodeDocInconsistency(lib, version, contract_name, func_name, level)
        else:
            checkContractCodeDocInconsistency(lib, version, contract_name, level)
