#!/usr/bin/python3
"""Defines a function that distributes an archive"""

import os.path
from fabric import Connection, task

remote_hosts = ['34.203.29.40', '54.164.120.187']


@task
def do_deploy(c, archive_path):
    """
    Distributes an archive to a web server

    Args:
        c (Connection): Fabric Connection object.
        archive_path (str): The path of the archive to distribute.
    Returns:
        True if all operations have been done correctly, otherwise False.
    """
    if not os.path.isfile(archive_path):
        return False

    file = os.path.basename(archive_path)
    name = os.path.splitext(file)[0]

    # Upload the archive to the servers
    with Connection(c) as conn:
        result = conn.put(archive_path, f"/tmp/{file}", use_sudo=True)
        if result.failed:
            return False

    for host in remote_hosts:
        with Connection(host) as conn:
            with conn.prefix("sudo"):
                # Uncompress the archive
                conn.run("mkdir -p /data/web_static/releases/{}/".format(name))
                conn.run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
                         .format(file, name))
                conn.run("rm /tmp/{}".format(file))

                # Update symbolic links
                conn.run("mv /data/web_static/releases/{}/web_static/*\
                         /data/web_static/releases/{}/".format(name, name))
                conn.run("rm -rf /data/web_static/releases/{}/web_static"
                         .format(name))

                conn.run("rm -rf /data/web_static/current")
                conn.run("ln -s /data/web_static/releases/{}/\
                         /data/web_static/current".format(name))

    return True
