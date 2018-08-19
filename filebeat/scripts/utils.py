import os
from subprocess import Popen, PIPE, STDOUT
from datetime import datetime as dt
from datetime import timedelta


def get_relative_path(relative_path):
    file_abs_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(file_abs_path, relative_path)

def get_date_time():
    x = str(dt.now())
    x = x.replace('.', '-')
    x = x.replace(':', '-')
    x = x.replace(' ', '-')
    return x

def exec_bash_command(command):
    p = Popen(command.split(), stdout=PIPE)
    stdout, stderr = p.communicate()
    exit_code = str(p.returncode)
    return {
        'exit_code': exit_code,
        'stdout': stdout,
        'stderr': stderr
    }

def create_call_dir(timestamp):
    dir_path = get_relative_path('../call-history/{0}'.format(timestamp))
    command = "mkdir " + dir_path
    exec_bash_command(command)

def move_txt_file(timestamp, file_path):
    dir_path = get_relative_path('../call-history/{0}/data'.format(timestamp))
    mkdir_command = 'mkdir ' + dir_path
    move_command = "mv {0} {1}".format(file_path, dir_path)
    exec_bash_command(mkdir_command)
    exec_bash_command(move_command)
