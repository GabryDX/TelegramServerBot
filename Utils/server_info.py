#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""File con info su Raspberry Pi"""

import os


def get_all_info():
    str = ""
    server = get_raspberry_model()
    if server:
        str += "Server: " + server
    os_info = get_os_info()
    if os_info:
        str += "\nOS: " + os_info
    str += "\nCPU modello: " + get_cpu_model_name()
    cpu_temp = get_cpu_temperature()
    if cpu_temp:
        str += "\nCPU Temperatura: " + cpu_temp + " °C"
    str += "\nCPU usata: " + get_cpu_use() + " %"
    ram = get_ram_info()
    str += "\nRAM totale: " + ram[0] + " KB"
    str += "\nRAM usata: " + ram[1] + " KB"
    str += "\nRAM libera: " + ram[2] + " KB"
    disk = get_disk_space()
    str += "\nSpazio totale: " + disk[0] + "B"
    str += "\nSpazio usato: " + disk[1] + "B (" + disk[3] + ")"
    str += "\nSpazio rimanente: " + disk[2] + "B"
    return str.strip()


# Return CPU model name
def get_cpu_model_name():
    res = os.popen('cat /proc/cpuinfo | grep "model name" | head -n 1')
    res = res.read().replace("model name\t:", "").strip()
    return res


# Return CPU temperature as a character string
def get_cpu_temperature():
    res = os.popen('vcgencmd measure_temp').readline()
    if "not found" in res:
        res = os.popen('sensors | grep "Package id" | head -n 1 cut -d"\\"" -f5')
        return res[1:-2]
    else:
        return res.replace("temp=", "").replace("'C\n", "")


# Return RAM information (unit=kb) in a list
# Index 0: total RAM
# Index 1: used RAM
# Index 2: free RAM
def get_ram_info():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return line.split()[1:4]


# Return % of CPU used by user as a character string
def get_cpu_use():
    # return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))
    lista = os.popen("ps aux | awk '{print $3}'")
    cpu = 0.0
    for l in lista:
        riga = l.strip()
        if "CPU" not in riga:
            cpu += float(riga)
    return str(round(cpu, 2))


# Return information about disk space as a list (unit included)
# Index 0: total disk space
# Index 1: used disk space
# Index 2: remaining disk space
# Index 3: percentage of disk used
def get_disk_space():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i == 2:
            return line.split()[1:5]


def get_os_info():
    res = os.popen('cat /etc/os-release | grep "NAME" | head -n 1 | cut -d"\\"" -f2')
    res = res.read().strip()
    return res


def get_raspberry_model():
    res = os.popen('cat /sys/firmware/devicetree/base/model')
    res = res.read().strip()
    return res
