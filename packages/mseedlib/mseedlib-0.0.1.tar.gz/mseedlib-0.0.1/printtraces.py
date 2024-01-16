#!/usr/bin/env python3

import sys
import argparse
from mseedlib import MSTraceList


# Parse command line arguments
parser = argparse.ArgumentParser(description='Print trace listing from specified miniSEED files')
parser.add_argument('--verbose', '-v', action='count', default=0,
                    help='Increase verbosity')
parser.add_argument('--unpack', '-u', action='store_true',
                    help='Unpack (decode) data samples')
parser.add_argument('input_files', nargs=argparse.REMAINDER,
                    help='Input miniSEED files')
args = parser.parse_args()


mstl = MSTraceList()

for arg in args.input_files:
    mstl.readFile(arg, unpack_data=args.unpack, verbose=args.verbose)

#tid = next(mstl.traceids())
#seg = next(tid.segments())

mstl.print()

