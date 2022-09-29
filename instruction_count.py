#!/usr/bin/env python3

"""
This is a script to read cosim instruction log and give the unique instruction number
"""

import sys
import os
import gzip
from pathlib import Path


def get_inst_code_list(list1):
    """
    Slice the instruction machine code by extracting the code in the 1st brackets
    >>> line = "core   0: 0x0000000080000000 (0x00000517) auipc   a0, 0x0"
    >>> get_inst_code_list([line])
    ["0x00000517"]
    """
    code_list = [inst.split('(',1)[-1].split(')')[0] for inst in list1]
    return code_list

def get_inst_cmd_list(list1):
    """
    Extract the instruction opcode from unprevilaged instruction lines.
    >>> line = "core   0: 0x0000000080000000 (0x00000517) auipc   a0, 0x0"
    >>> get_inst_cmd_list([line])
    ["auipc"]
    """
    cmd_list = [inst.split(')',1)[-1].split()[0] for inst in list1]
    return cmd_list

def check_privilege(line):
    """
    >>> line = "core   0: 3 0x0000000080000000 (0x00000517) x10 0x0000000080000000"
    >>> check_privilege(line)
    True
    >>> line = "core   0: 0x0000000080000000 (0x00000517) auipc   a0, 0x0"
    >>> check_privilege(line)
    False
    """
    n = len(line.split('(',1)[0].split())
    return n == 4

## To modify: make usre input
proj = "/scratch/mwu/federation/builds/coreip_s76/"

tmp1 = list(Path(proj).rglob('cosim.log.gz'))
# Open file and driven code
for cosimlog in tmp1:
    print("==============================================")
    print(cosimlog)

    with gzip.open(cosimlog,'r') as fp:
        # Grouping lines by privilege or unprivilege
        privilege, unprivilege = [],[]
        for line in fp:
            line_str = line.decode()
            if check_privilege(line_str):
                privilege.append(line_str)
            else:
                unprivilege.append(line_str)

        #print("=== Privilege lines preview, Total ", len(privilege) ," lines ===")
        #print("\n".join(privilege[0:5]))
        #print(f"=== Unprivilege lines preview, Total ", len(unprivilege)," lines ===")
        #print("\n".join(unprivilege[0:5]))

        # Get instructions for privileged ISA
        privilege_inst_code_list = get_inst_code_list(privilege)


        # Get instructions for unprivileged ISA
        unprivilege_inst_code_list = get_inst_code_list(unprivilege)
        unprivilege_inst_cmd_list = get_inst_cmd_list(unprivilege)

        #print("=== unprivilege command preview ===")
        #print("\n".join(unprivilege_inst_cmd_list[0:5]))

        # Find uniqe instructions from unprivilege instruction commands
        uniqe_inst_list = set(unprivilege_inst_cmd_list)
        print("*** There are ", len(uniqe_inst_list)," unique instructions:")
        print("=== Unique instruction list ===")
        print(uniqe_inst_list)

