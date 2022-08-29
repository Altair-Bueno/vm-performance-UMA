"""
name: "Práctica 6: Prestaciones de la virtualización. util.py"
subtitle: |
    Funciones de ayuda para cargar los datos
author:
    - "Altair Bueno <altair.bueno@uma.es>"
date: 2022-8-29
keywords:
    - "Arquitecturas virtuales"
    - "Ingeniería del software"
    - "Práctica 6"
"""
import json
from re import compile, MULTILINE, DOTALL

import polars as pl

NAME = "name"
COMMAND = "command"
TASK_CLOCK = "task_clock"
CPUS_UTILIZED = "cpus_utilized"
CONTEXT_SWITCHES = "context_switches"
CONTEXT_SWITCHES_SPEED = "context_switches_speed"
CPU_MIGRATIONS = "cpu_migrations"
CPU_MIGRATIONS_SPEED = "cpu_migrations_speed"
PAGE_FAULTS = "page_faults"
PAGE_FAULTS_SPEED = "page_faults_speed"
CYCLES = "cycles"
CYCLES_HZ = "cycles_hz"
INSTRUCTIONS = "instructions"
INSTRUCTIONS_PER_CYCLE = "ins_per_cycle"
BRANCHES = "branches"
BRANCHES_SPEED = "branches_speed"
BRANCH_MISSES = "branch_misses"
BRANCH_MISSES_PERCENTAGE = "branch_misses_percentage"
TOTAL = "total"

HEADERS = [
    NAME, COMMAND, TASK_CLOCK, CPUS_UTILIZED, CONTEXT_SWITCHES,
    CONTEXT_SWITCHES_SPEED, CPU_MIGRATIONS, CPU_MIGRATIONS_SPEED, PAGE_FAULTS,
    PAGE_FAULTS_SPEED, CYCLES, CYCLES_HZ, INSTRUCTIONS, INSTRUCTIONS_PER_CYCLE,
    BRANCHES, BRANCHES_SPEED, BRANCH_MISSES, BRANCH_MISSES_PERCENTAGE, TOTAL
]

assert len(HEADERS) == 19

__sample__ = """
ajsfaslf lkas flasjf klajslkfd
as df
as
 dfa
 f 
 sd
 Performance counter stats for 'sleep 5':

          0,551441      task-clock (msec)         #    0,000 CPUs utilized          
                 1      context-switches          #    0,002 M/sec                  
                 0      cpu-migrations            #    0,000 K/sec                  
                61      page-faults               #    0,111 M/sec                  
         1.149.305      cycles                    #    2,084 GHz                    
           860.972      instructions              #    0,75  insn per cycle         
           168.087      branches                  #  304,814 M/sec                  
             7.664      branch-misses             #    4,56% of all branches        

       5,000969694 seconds time elapsed
"""

# Only god knows how to read this RegEx
REGEX = compile(
    # Performance counter stats for 'sleep 5':
    r".*Performance counter stats for (?P<command>.+):\W+"
    # 0,551441      task-clock (msec)         #    0,000 CPUs utilized
    r"(?P<task_clock>[0-9,.]+)\W+task-clock \(msec\)[#\W]*(?P<cpus_utilized>[0-9,.]+)\W+CPUs utilized\W+"
    # 1      context-switches          #    0,002 M/sec
    r"(?P<context_switches>[0-9,.]+)\W+context-switches[#\W]*(?P<context_switches_speed>[0-9,.]+)\W+./sec\W+"
    # 0      cpu-migrations            #    0,000 K/sec         
    r"(?P<cpu_migrations>[0-9,.]+)\W+cpu-migrations[#\W]*(?P<cpu_migrations_speed>[0-9,.]+)\W+./sec\W+"
    # 61      page-faults               #    0,111 M/sec  
    r"(?P<page_faults>[0-9,.]+)\W+page-faults[#\W]*(?P<page_faults_speed>[0-9,.]+)\W+./sec\W+"
    # 1.149.305      cycles                    #    2,084 GHz
    r"(?P<cycles>[0-9,.]+)\W+cycles[#\W]*(?P<cycles_hz>[0-9,.]+)\W+.Hz\W+"
    # 860.972      instructions              #    0,75  insn per cycle
    r"(?P<instructions>[0-9,.]+)\W+instructions[#\W]*(?P<ins_per_cycle>[0-9,.]+)\W+insn per cycle\W+"
    # 168.087      branches                  #  304,814 M/sec
    r"(?P<branches>[0-9,.]+)\W+branches[#\W]*(?P<branches_speed>[0-9,.]+)\W+./sec\W+"
    # 7.664      branch-misses             #    4,56% of all branches
    r"(?P<branch_misses>[0-9,.]+)\W+branch-misses[#\W]*(?P<branch_misses_percentage>[0-9,.]+)%\W+of all branches\W+"
    # 5,000969694 seconds time elapsed
    r"(?P<total>[0-9,.]+) seconds time elapsed"
    r".*",
    MULTILINE | DOTALL
)


def extract(file) -> list[dict[str, str]]:
    """Transform the raw perf output into a list of dicts"""

    def process(d):
        return {k: v.replace('.', '').replace(',', '.') for k, v in d.items()}

    return [{"name": k} | process(REGEX.match(e).groupdict()) for k, v in
            json.load(file).items() for e in v]


def convert(df: pl.DataFrame) -> pl.DataFrame:
    """Casts raw values into usable data"""
    strings = [NAME, COMMAND]
    floating = [v for v in HEADERS if v not in strings]

    return df.select(
        strings +
        [pl.col(col).cast(pl.Float64) for col in floating]
    )


def load_polars_df(file) -> pl.DataFrame:
    dicts = extract(file)
    return convert(pl.from_dicts(dicts))
