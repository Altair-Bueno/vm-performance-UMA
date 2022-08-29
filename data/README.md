# Datos recogidos

## `cat /proc/cpuinfo`

- [`host_info.txt`](host_info.txt)
- [`guest_info.txt`](guest_info.txt)

## `uname -a`

- [`host_uname.txt`](host_uname.txt)
- [`guest_uname.txt`](guest_uname.txt)

## `free`

- [`host_mem.txt`](host_mem.txt)
- [`guest_mem.txt`](guest_mem.txt)

## `cat /etc/*release*`

- [`host_release.txt`](host_release.txt)
- [`guest_release.txt`](guest_release.txt):

## Scripts de python

- `host_bench.json`: [performance_host.py](../src/performance_host.py)
- `with_vm_bench.json`: [performance_virtualbox.py](../src/performance_virtualbox.py)
- `without_vm_bench.json`: [performance_virtualbox.py](../src/performance_virtualbox.py)