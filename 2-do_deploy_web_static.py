#!/usr/bin/python3
"""defines a function that distribute an archive"""
import os.path
from fabric.api import env, put, run

env.hosts = ['34.203.29.40', '54.164.120.187']
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_deploy(archive_path):
    """Distributes an archive to a web server"""

    try:
        if os.path.isfile(archive_path) is False:
            return False
        file = archive_path.split('/')[-1]
        name = file.split('.')[0]

        put(archive_path, "/tmp/{}".format(file))
        run("rm -rf /data/web_static/releases/{}/".format(name))
        run("mkdir -p /data/web_static/releases/{}/".format(name))

        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file,
                                                                       name))

        run("rm /tmp/{}".format(file))
        run("mv /data/web_static/releases/{}/web_static/* \
        /data/web_static/releases/{}/".format(name, name))

        run("rm -rf /data/web_static/releases/{}/web_static".format(name))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ \
        /data/web_static/current".format(name))
        return True

    except Exception:
        return False
