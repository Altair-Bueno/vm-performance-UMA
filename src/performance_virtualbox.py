#!/usr/bin/env python3.10
"""
name: "Práctica 6: Prestaciones de la virtualización. performance_virtualbox.py"
subtitle: |
    Ejecuta pruebas de rendimiento en la máquina guest
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

import paramiko

# Commands to execute on guest
_COMMAND_LIST = [
    'sleep 1',
    'sleep 5',
    'sleep 10',
    '~/Desktop/codes/benchmarks/ddcopy.bash'
    '~/Desktop/codes/benchmarks/forkwait',
    '~/Desktop/codes/benchmarks/pi.bc'
]

# Number of samples
_NUMBER_TEST = 10

class SSH:
    def __init__(self,ip,username,password) -> None:
        self.ip = ip
        self.username = username
        self.password = password
    def init_shell(self):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.ip,username=self.username,password=self.password,look_for_keys=False)
        return client


def launch(virtualbox_pid,connection:paramiko.SSHClient):
    dic = {
        'ls':[]
    }
    # Analize virtualbox
    perf_command =  [
        "perf",
        "stat",
        "--pid",
        virtualbox_pid
    ]

    for command in _COMMAND_LIST:
        print(f'Executing {command}')
        dic[command] = []
        for i in range(_NUMBER_TEST):
            perf_pointer = Popen(perf_command, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
            stdin, stdout, stderr = connection.exec_command(command)
            exit_code = stdout.channel.recv_exit_status()
            if exit_code != 0:
                print(f'Non zero exit status: {exit_code}')
            perf_pointer.send_signal(2) # SIGINT ^C
            result = perf_pointer.stdout
            dic[command].append(result.read().decode("utf-8"))

    for i in range(_NUMBER_TEST):
        perf_pointer = Popen(perf_command, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        connection.exec_command('ls')
        perf_pointer.send_signal(2) # SIGINT ^C
        result = perf_pointer.stdout
        dic['ls'].append(result.read().decode("utf-8"))
    return dic
        


def main():
    # Obtain input
    ip = input("Insert guest IP: ")
    username = input("Insert guest username: ")
    password = input("Insert guest password: ")
    virtualbox_pid = input("Insert virtualbox PID: ")
    output_path = input("Output path: ")
    ssh = SSH(ip,username,password)

    # Stablish a SSH connection
    connection = ssh.init_shell()
    # Launch
    dic = launch(virtualbox_pid,connection)
    json = dumps(dic)
    with open(output_path,'wt') as output_file:
        output_file.write(json)
    # Close ssh session
    connection.close()
    

if __name__ == '__main__':
    main()