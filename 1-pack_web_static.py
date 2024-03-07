#!/usr/bin/python3
"""generates a .tgz archive from a folder"""
from fabric.api import local
from datetime import datetime
from os.path import isdir


def do_pack():
    """ creates a .tgz archive """
    dt = datetime.utcnow()
    file_name = f"versions/web_static_{dt.year}{dt.month}{dt.day}{dt.hour}"
    if isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None

    if local(f"tar -czvf {file_name} web_static").failed is True:
        return None
    else:
        return file_name
