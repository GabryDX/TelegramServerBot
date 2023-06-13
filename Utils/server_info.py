#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""File con info su Raspberry Pi"""

import os
import platform


def get_all_info():
    info_str = ""
    platform_system = platform.system()
    if platform_system == "Linux":
        server = get_raspberry_model()
        if server:
            info_str += "Server: " + server
        os_info = get_os_info()
        if os_info:
            info_str += "\nOS: " + os_info
        cpu_info = get_cpu_info()
        if cpu_info:
            info_str += "\nCPU:"
            if "model_name" in cpu_info:
                info_str += "\n |- modello: " + cpu_info["model_name"]
            if "temperature" in cpu_info:
                info_str += "\n |- temperatura: " + cpu_info["temperature"] + " °C"
            if "usage" in cpu_info:
                info_str += "\n |- usata: " + cpu_info["usage"] + " %"
        ram = get_ram_info()
        if ram:
            info_str += "\nRAM:"
            info_str += "\n |- totale: " + ram[0] + " KB (" + str(convert_KB_to_GB(float(ram[0]), 2)) + " GB)"
            info_str += "\n |- usata: " + ram[1] + " KB (" + str(convert_KB_to_GB(float(ram[1]), 2)) + " GB)"
            info_str += "\n |- libera: " + ram[2] + " KB (" + str(convert_KB_to_GB(float(ram[2]), 2)) + " GB)"
        disk = get_disk_space()
        if disk:
            info_str += "\nSpazio:"
            info_str += "\n |- totale: " + disk[0] + "B"
            info_str += "\n |- usato: " + disk[1] + "B (" + disk[3] + ")"
            info_str += "\n |- rimanente: " + disk[2] + "B"
        adapters = get_adapters()
        if adapters:
            info_str += adapters
    else:
        info_str = "Current server: " + platform_system
    return info_str.strip()


# Return CPU model name
def get_cpu_model_name():
    res = os.popen('cat /proc/cpuinfo | grep "model name" | head -n 1')
    res = res.read().replace("model name\t:", "").strip()
    return res


# Return CPU temperature as a character string
def get_cpu_temperature():
    res = os.popen('vcgencmd measure_temp').readline()
    if "not found" in res:
        res = os.popen('sensors | grep "Package id" | head -n 1 | cut -d" " -f5')
        return res[1:-2]
    else:
        return res.replace("temp=", "").replace("'C\n", "")


# Return % of CPU used by user as a character string
def get_cpu_usage():
    # return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip()))
    lista = os.popen("ps aux | awk '{print $3}'")
    cpu = 0.0
    for l in lista:
        riga = l.strip()
        if "CPU" not in riga:
            cpu += float(riga)
    return str(round(cpu, 2))


# Return CPU info in a dictionary
def get_cpu_info():
    cpu_dict = dict()
    model_name = get_cpu_model_name()
    temperature = get_cpu_temperature()
    usage = get_cpu_usage()
    if model_name:
        cpu_dict["model_name"] = model_name
    if temperature:
        cpu_dict["temperature"] = temperature
    if usage:
        cpu_dict["usage"] = usage
    return cpu_dict


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


def convert_KB_to_GB(kb, round_index):
    return round(kb / (1024 * 1024), round_index)


def get_adapters():
    res = os.popen('sensors').read()
    res = res.replace("        ", "\t").strip()
    sensors = res.split("\n\n")
    new_res = "\nAdapters:"
    for sensor in sensors:
        details = sensor.strip().split("\n")
        if "Adapter:" not in details[0]:
            details[1] += " - " + details[0]
            details.pop(0)
        name_adapter = details[0].replace("Adapter:", "", 1).strip()
        new_res += "\n |- " + name_adapter
        for detail in details[1:]:
            new_detail = detail.replace("\t", " ").replace("  ", " ").strip()
            if new_detail == "" or new_detail.startswith(" ") or new_detail.startswith("("):
                pass
            else:
                id_parenthesis = new_detail.index("(")
                if id_parenthesis > -1:
                    new_detail = new_detail[:id_parenthesis]
                new_res += "\n |-|- " + new_detail.strip()
    return new_res


def run_command(command: str) -> str:
    try:
        return os.popen(command).read().strip()
    except Exception as e:
        return str(e)
