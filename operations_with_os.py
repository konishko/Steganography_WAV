#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def read_bytes_from_file(file_name):
    with open(file_name, 'rb') as file:
        return file.read()


def write_bytes_to_file(bytes, file_name):
    with open(file_name, 'wb') as file:
        file.write(bytes)


def get_free_name(name):
    index = 1
    if os.path.exists(name):
        while(True):
            if os.path.exists('({}){}'.format(index, name)):
                index += 1
            else:
                name = '({}){}'.format(index, name)
                break
    return name
