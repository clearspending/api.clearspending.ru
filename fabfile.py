# -*- coding: utf-8 -*-

from fabric.api import local
from fabric.state import env
import os

env.hosts = ['localhost']

def teamcity_kill_api():
    try:
        local('pkill -9 -f "api/tornading.py API 9080"')
        local('pkill -9 -f "api/tornading.py API 9081"')
        local('pkill -9 -f "api/tornading.py API 9082"')
    except:
        print('test API not running')
    return 0


def teamcity_install_venv():
    project_root = local('pwd', capture=True)

    os.environ["PYTHONPATH"] = project_root
    local('virtualenv-2.7 venv')
    local('./venv/bin/pip2.7 install -r deploy/requirments.txt')
    return 0


def teamcity_start_api():
    project_root = local('pwd', capture=True)
    os.environ["PYTHONPATH"] = project_root
    local('mkdir -p logs', capture=True)
    local('nohup ./venv/bin/python2.7 api/tornading.py API 9080 > logs/log_api_9080 2>&1 &')
    local('nohup ./venv/bin/python2.7 api/tornading.py API 9081 > logs/log_api_9081 2>&1 &')
    local('nohup ./venv/bin/python2.7 api/tornading.py API 9082 > logs/log_api_9082 2>&1 &')
    return 0


def teamcity_create_local_settings_file():
    project_root = local('pwd', capture=True)

    os.environ["PYTHONPATH"] = project_root
    with open('common/local_settings.py', 'w+') as f:
        f.writelines([
            "MONGO_SERVER = '127.0.0.1'# dev2\n",
            "SPHNX_IP = '127.0.0.1'\n",
            "SPHNX_PORT = 3314\n",
            "MONGO_PORT = 27017\n",
            "MEMCACHE_ENABLED = False\n",
            ])