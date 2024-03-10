#!/usr/bin/python3
"""defines a function that distribute an archive"""
import os.path
from fabric import Connection, task
remote_hosts = ['34.203.29.40', '54.164.120.187']

@task
def do_deploy(c, archive_path):
    """Distributes an archive to a web server"""
    if not os.path.isfile(archive_path):
        return False

    file = os.path.basename(archive_path)
    name = os.path.splitext(file)[0]

    for host in remote_hosts:
        with Connection(c):
            result = c.put(archive_path, "/tmp/{}".format(file), use_sudo=True)
            if result.failed:
                return False

            with c.prefix("sudo"):
                c.run("rm -rf /data/web_static/releases/{}/".format(name))
                c.run("mkdir -p /data/web_static/releases/{}/".format(name))
                c.run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name))
                c.run("rm /tmp/{}".format(file))
                c.run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name))
                c.run("rm -rf /data/web_static/releases/{}/web_static".format(name))

            c.run("rm -rf /data/web_static/current")
            c.run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name))

    return True
