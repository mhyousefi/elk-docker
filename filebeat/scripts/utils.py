import os
from subprocess import Popen, PIPE, STDOUT
from datetime import datetime as dt
from datetime import timedelta


my_path = os.path.abspath(os.path.dirname(__file__))

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
    dir_path = os.path.join(my_path, '../call-history/' + timestamp)
    command = "mkdir " + dir_path
    exec_bash_command(command)

def move_txt_file(timestamp, file_path):
    dir_path = os.path.join(my_path, '../call-history/{0}/data'.format(timestamp))
    mkdir_command = 'mkdir ' + dir_path
    move_command = "mv {0} {1}".format(file_path, dir_path)
    exec_bash_command(mkdir_command)
    exec_bash_command(move_command)
