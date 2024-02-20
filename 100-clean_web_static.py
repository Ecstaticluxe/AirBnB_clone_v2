#!/usr/bin/python3
"""
A Fabric script (based on the file 3-deploy_web_static.py)
that deletes out-of-date archives, using the function do_clean:
"""
import os
from fabric.api import *

env.user = "ubuntu"
env.hosts = ['54.90.34.141', '34.229.49.23']


def get_files(action, dir_path):
    """
    Gets files in a dir and returns a list of them
    dir_path: path to directory to fetch files from
    action: by what mean to carry actions (local, run)

    return: list of filename in the directory
    """
    # dictionary of actions
    action_dict = {'local': lambda x: local(x, capture=True), 'run': run}
    # get files in archive
    # read all file in dir by pathname and get the
    # file basename
    my_action = action_dict.get(action, local)
    dir_content = (my_action(f'ls {dir_path}')).split()
    return list(filter(lambda x: x.startswith("web_static_"), dir_content))


def get_max(archives):
    """
    Gets the maximum from a list of web_static archives
    archives: archive list to traverse

    return: maximum or most current archive
    """
    # strip off web_static_ and .tgz and get the num form of archives
    coat = "web_static_.tgz"  # archive coat
    archive_mapper = list(map(lambda x: int(x.strip(coat)), archives))
    # encoat with web_static_.tgz
    try:
        return f'web_static_{max(archive_mapper, key=int)}.tgz'
    except Exception:
        return None


@task
def do_clean(number=0):
    """
    A fabric task that removes out of date archive from
    /data/web_static/releases

    numbers: numbers of most recent archive to keep
    """
    def operate(action, path):
        """
        Performs cleaning operations
        action: by what mean to carry actions (local, run)
        path: path to carry out actions on

        return: None
        """
        # dictionary of actions
        action_dict = {'local': local, 'run': run}
        # get archive list and right action
        archives = get_files(action, path)
        my_action = action_dict.get(action, local)
        if action == "run":
            archives = list(map(lambda x: x.strip(".tgz"), archives))

        # loop remove all most recent archives to be kept
        kept = 0
        # for servers folders do not have .tgz
        is_server = action == "run"
        while kept < number:
            if not archives:
                break
            max = (get_max(archives).strip(".tgz") if is_server
                   else get_max(archives))
            print(f'max ->  {max}')
            archives.remove(max)
            kept += 1
        # delete archives left
        for archive in archives:
            my_action(f'rm -rf {path}{archive}')

    number = int(number)
    operate('local', './versions/')
    operate('run', '/data/web_static/releases/')
