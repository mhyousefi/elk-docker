from subprocess import Popen, PIPE, STDOUT
from datetime import datetime as dt
from datetime import timedelta

def get_date_time():
    return str(dt.now()).replace(' ', '-')

def exec_bash_command(command):
    p = Popen(command.split(), stdout=PIPE)
    stdout = p.communicate()[0]
    exit_code = p.returncode
    return (exit_code, stdout)

def create_call_dir(timestamp):
    command = "mkdir ../call-history/" + timestamp
    exec_bash_command(command)

def move_txt_file(file_path, timestamp):
    mkdir_command = 'mkdir ../call-history/{0}/data'.format(timestamp)
    exec_bash_command(mkdir_command)

    move_command = "mv {0} ../call-history/{1}/data".format(file_path, timestamp)
    exec_bash_command(move_command)
