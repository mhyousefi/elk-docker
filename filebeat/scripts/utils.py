from subprocess import Popen, PIPE, STDOUT
from datetime import datetime as dt
from datetime import timedelta

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
    command = "mkdir ../call-history/" + timestamp
    exec_bash_command(command)

def move_txt_file(timestamp, file_path):
    mkdir_command = 'mkdir ../call-history/{0}/data'.format(timestamp)
    exec_bash_command(mkdir_command)

    move_command = "mv {0} ../call-history/{1}/data".format(file_path, timestamp)
    exec_bash_command(move_command)
