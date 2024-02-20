#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive from
the contents of the web_static folder of your AirBnB Clone
repo, using the function do_pack.
"""
from fabric.api import *
from datetime import datetime as dt
import os

# env.hosts = ['ubuntu@34.229.49.23', 'ubuntu@54.90.34.141']
# env.user = "ubuntu"


@task
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
