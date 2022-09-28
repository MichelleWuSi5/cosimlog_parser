#!/usr/bin/python3.6

#This is a script to read cosim instruction log and give the unique instruction number

import sys,os
import gzip
from pathlib import Path

encoding = 'utf-8'


proj= "/scratch/mwu/federation/builds/coreip_s76/"
tmp1 =list(Path(proj).rglob('cosim.log.gz'))




debug_level = 0


#Find unique value in the list
def unique(list1):
    #insert the list to the set
    list_set = set(list1)

    #convert the set to the list
    unique_list = (list(list_set))
    return unique_list


def get_inst_code_list(list1):
    #slice the instruction machine code by extracting the ocde in the 1st brackets
    code_list = [inst.split('(',1)[-1].split(')')[0] for inst in list1]
    return code_list

def get_inst_cmd_list(list1):
    cmd_list = [inst.split(')',1)[-1].split()[0] for inst in list1]
    return cmd_list

def check_privilege(line):
    n =len(line.split('(',1)[0].split())
    if n==4:
        return True
    else:
        return False

#open file and driven code
for cosimlog in tmp1:
    print("==============================================")
    print(cosimlog)
    with gzip.open(cosimlog,'r') as fp:
        #put every lines of the file content as a list
        lines = list(fp)

        #grouping lines by privilege or unprivilege
        privilege, unprivilege = [],[]
        for line in lines:
            line_str = line.decode(encoding)
            #(unprivilege, privilege)[check_privilege(line_str)].append(line_str)
            if check_privilege(line_str):
                privilege.append(line_str)
            else:
                unprivilege.append(line_str)

        if debug_level ==1:
            print(f"=== privilege lines preview, Total {len(privilege)} lines ===")
            for i in privilege[0:5]: print(i)
            print(f"=== Unprivilege lines preview, Total {len(unprivilege)} lines ===")
            for i in unprivilege[0:5]: print(i)

        #get instructions
        privilege_inst_code_list = get_inst_code_list(privilege)


        #get instructions for unprivileged ISA
        unprivilege_inst_code_list = get_inst_code_list(unprivilege)
        unprivilege_inst_cmd_list = get_inst_cmd_list(unprivilege)

        if debug_level ==1:
            print(f"=== unprivilege command preview ===")
            for i in unprivilege_inst_cmd_list[0:5]: print(i)

        #find uniqe instructions from unprivilege instruction commands
        uniqe_inst_list = unique(unprivilege_inst_cmd_list)
        print(f"=== Unique instruction list ===")
        print(f">> There are {len(uniqe_inst_list)} unique instructions:")
        print(uniqe_inst_list)
        #print(len(uniqe_inst_list))

        fp.close()

