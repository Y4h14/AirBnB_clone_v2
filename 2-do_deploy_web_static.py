#!/usr/bin/python3
"""defines a function that distribute an archive"""
import os.path
from fabric.api import env, put, run
env.host = ['34.203.29.40', '54.164.120.187']


def do_deploy(archive_path):
    """Distributes an archive to a web server"""
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_bath.split('/')[-1]
    name = file.split('.')[0]

    if put(arvhive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -c /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ \
            /data/web_static/current".format(name)).failed is True:
        return False
    return True