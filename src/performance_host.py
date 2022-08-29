#!/usr/bin/env python3.10
"""
name: "Práctica 6: Prestaciones de la virtualización. performance_host.py"
subtitle: |
    Ejecuta pruebas de rendimiento en la máquina host
author:
    - "Altair Bueno <altair.bueno@uma.es>"
date: 2021-12-29
keywords:
    - "Arquitecturas virtuales"
    - "Ingeniería del software"
    - "Práctica 6"
"""
from json import dumps
from subprocess import PIPE, STDOUT, Popen

# Commands to execute on host
_COMMAND_LIST = {
    'sleep1': ['sleep','1'],
    'sleep5': ['sleep','5'],
    'sleep10': ['sleep','10'],
    'ddcopy': ['./material/benchmarks/codes/ddcopy.bash'],
    'forkwait': ['./material/benchmarks/codes/forkwait'],
    'pi': ['./material/benchmarks/codes/pi.bc']
}

# Number of samples
_NUMBER_TEST = 10

def main():
    filename = input("Name of output file: ")
    dic = {}
    for name,command in _COMMAND_LIST.items():
        dic[name] = []
        for i in range(_NUMBER_TEST):
            perf_command = [
                "perf",
                "stat"
            ]
            perf_command.extend(command)
            print(f'executing {name}: {command}')
            proccess = Popen(perf_command, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
            proccess.wait()
            res = proccess.stdout.read().decode("utf-8")
            dic[name].append(res)
    json_string = dumps(dic)
    # print(json_string)
    with open(filename,'wt') as file:
        file.write(json_string)



if __name__ == '__main__':
    main()