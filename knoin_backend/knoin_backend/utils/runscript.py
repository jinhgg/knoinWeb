import os


def runscript(cmd: str) -> list:
    return_list = []
    output = os.popen(cmd).readlines()
    for line in output:
        return_list.append(line)
    return return_list
