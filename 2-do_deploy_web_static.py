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
        dir_path = "/data/web_static/releases/"
        filename = os.path.basename(archive_path)
        file_no_ext, ext = os.path.splitext(filename)
        put(archive_path, "/tmp/{}".format(filename))
        run("rm -rf {}{}".format(dir_path, file_no_ext))
        run("mkdir -p {}{}".format(dir_path, file_no_ext))
        run("tar -xzf /tmp/{} -C {}{}".format(filename, dir_path, file_no_ext))
        run("rm /tmp/{}".format(filename))
        run("mv {0}{1}/web_static/* {0}{1}/".format(dir_path, file_no_ext))
        run("rm -rf {}{}/web_static".format(dir_path, file_no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(
            dir_path, file_no_ext))
        return True

    except Exception:
        return False
