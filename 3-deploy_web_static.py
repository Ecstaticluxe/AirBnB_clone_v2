#!/usr/bin/python3
"""
A Fabric script (based on the file 2-do_deploy_web_static.py)
that creates and distributes an archive to your web servers,
using the function deploy:
"""
from fabric.api import *
import os
from datetime import datetime as dt

def do_pack():
    """
    a function that generates a .tgz archive from
    the contents of the web_static folder of your AirBnB Clone
    repo, using the function do_pack.
    """
    today = dt.now()
    day = today.day
    month = today.month
    year = today.year
    hour = today.hour
    mins = today.minute
    sec = today.second

    f_date = f"{year}{month}{day}{hour}{mins}{sec}"
    tar_name = f"web_static_{f_date}.tgz"
    print(f'Packing web_static to versions/{tar_name}')

    local("mkdir -p versions")
    archive = local(f"tar -czvf versions/{tar_name} ./web_static")
    size = os.path.getsize(f"versions/{tar_name}")
    print(f'web_static packed: verions/{tar_name} -> {size}Bytes')

    if archive.succeeded:
        return f"versions/{tar_name}"
    return None

def do_deploy(archive_path):
    """
    a Fabric task (based on the file 1-pack_web_static.py)
    that distributes an archive to your web servers,
    using the function do_deploy:
    """

    if not os.path.exists(archive_path):
        return False

    # versions/
    # archive name = web_static_20170315003959
    # .tgz
    try:
        put(archive_path, '/tmp')
        archive_name = archive_path.split('/')[-1]
        unpacked = archive_name.split('.')[0]
        new_dir = unpacked
        with cd('/tmp'):
            run(f'mkdir -p /data/web_static/releases/{new_dir}')
            run(f'tar -xvzf {archive_name} -C\
                /data/web_static/releases/{new_dir}')
            sudo(f'rsync -a /data/web_static/releases/{new_dir}/web_static/* \
                /data/web_static/releases/{new_dir}')
            run(f'rm {archive_name}')
            run(f'rm -r /data/web_static/releases/{new_dir}/web_static/')
            run('rm /data/web_static/current')
            run(f'ln -sf /data/web_static/releases/{unpacked} \
                /data/web_static/current')
        return True
    except Exception:
        return False


env.user = 'ubuntu'
env.hosts = ['54.90.34.141', '34.229.49.23']


@task
def deploy():
    """
    A Fabric script (based on the file 2-do_deploy_web_static.py)
    that creates and distributes an archive to your web servers,
    using the function deploy:
    """
    packed = do_pack()
    if not packed or not os.path.exists(packed):
        return False
    do_deploy(packed)
    print("New version deployed!")
