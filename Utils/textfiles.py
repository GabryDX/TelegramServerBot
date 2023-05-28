#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Strumento per la gestione dei file .txt
"""

import errno
import io
import os


# ritorna il contenuto di un file come stringa
def read(filename):
    # with open(filename) as f:
    with io.open(filename, "r", encoding="utf-8") as f:
        data = f.readlines()
    return data


# scrive o sovrascrive un file con str
def write(str, filename):
    with io.open(filename, "w", encoding="utf-8") as f:
        f.write(str)


# aggiunge str al contenuto del file
def append(str, filename):
    with io.open(filename, "a", encoding="utf-8") as f:
        f.write(str)


# ritorna una lista di stringhe con le righe del file
def readLines(filename):
    # lines = open(filename).read().splitlines()
    # lines = io.open(filename, "r", encoding="utf-8").splitlines()
    lines = open(filename, encoding="utf-8-sig").read().splitlines()
    return lines


# ritorna True se il file esiste
def exists(filename):
    return os.path.isfile(filename)


def exists_dir(directory):
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def make_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# ritorna True se il file è vuoto
def isEmpty(filename):
    return os.stat(filename).st_size == 0


# aggiorna il contenuto della riga toUpdate con updated del file
def updateLine(toUpdate, updated, filename):
    lines = readLines(filename)

    newText = ""
    for s in lines:
        if s == toUpdate:
            newText += updated + "\n"
        else:
            newText += s + "\n"
    write(newText, filename)
