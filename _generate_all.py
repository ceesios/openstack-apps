#!/bin/env python

import os
import json
import logging

cwd = os.path.dirname(os.path.abspath(__file__))
if cwd == '':
    cwd = '.'

print cwd

struct = {}

def add_to_struct(os_type, os_distro, os_version, key, val):
    if not os_type in struct:
        struct[os_type] = {}
    if not os_distro in struct[os_type]:
        struct[os_type][os_distro] = {}
    if not os_version in struct[os_type][os_distro]:
        struct[os_type][os_distro][os_version] = {}

    struct[os_type][os_distro][os_version][key] = val

def add_metadata(directory, metadata):
    path, os_distro = os.path.split(directory)
    path, os_type = os.path.split(path)
    os_version, ext = os.path.splitext(metadata)

    with open(os.path.join(directory, metadata), 'rb') as fh:
        try:
            data = json.load(fh)
        except Exception as e:
            logging.exception(e)
            return

        add_to_struct(os_type, os_distro, os_version, 'metadata', data)
        print 'Imported metadata for %s' % os.path.join(os_type, os_distro, metadata)

def add_userdata(directory, userdata):
    path, os_distro = os.path.split(directory)
    path, os_type = os.path.split(path)
    os_version, ext = os.path.splitext(userdata)

    userdata_path = '/'.join([os_type, os_distro, userdata])
    add_to_struct(os_type, os_distro, os_version, 'userdata', userdata_path)
    print 'Added userdata for %s' % userdata_path

for (dirpath, dirnames, filenames) in os.walk(cwd):
    if '.git' in dirpath or not filenames:
        continue

    for file in filenames:
        if file[0] == '.':
            continue

        img, filetype = file.rsplit('.', 1)
        if filetype == 'metadata':
            add_metadata(dirpath, file)
        if filetype == 'userdata':
            add_userdata(dirpath, file)

if struct:
    with open(os.path.join(cwd, 'all.json'), 'wb') as fh:
        json.dump(struct, fh, indent=4, sort_keys=True)
