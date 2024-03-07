#!/usr/bin/python3
"""generates a .tgz archive from a folder"""
from fabric.api import local
from datetime import datetime
from os.path import isdir


def do_pack():
    """ creates a .tgz archive """
    dt = datetime.utcnow()
    file_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                          dt.month,
                                                          dt.day,
                                                          dt.hour,
                                                          dt.minute,
                                                          dt.second)
    if isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None

    if local("tar -czvf {} web_static".format(file_name)).failed is True:
        return None
    else:
        return file_name
