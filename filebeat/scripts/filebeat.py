import sys
from utils import get_date_time, exec_bash_command, create_call_dir, move_txt_file
from docker_commands import docker_compose_up, remove_container, rename_container
from docker_compose_config import create_docker_compose
from filebeat_config import create_filebeat_config

def create_call_folder(timestamp, data_file_path, index):
    exec_bash_command("mkdir -p ../call-history")
    create_call_dir(timestamp)
    create_docker_compose(timestamp)
    create_filebeat_config(timestamp, index)
    move_txt_file(timestamp, data_file_path)

try:
    DATA_FILE_PATH = sys.argv[1]
    INDEX = sys.argv[2]
    TIMESTAMP = get_date_time()
    DOCKER_COMPOSE_ADDR = "../call-history/{0}/docker-compose.yml".format(TIMESTAMP)
except:
    print("No arguments passed")
    exit(1)

try:
    create_call_folder(TIMESTAMP, DATA_FILE_PATH, INDEX)
except:
    print("Could not create the call folder")
    exit(1)

try:
    result = docker_compose_up(DOCKER_COMPOSE_ADDR)
except:
    print("Could not create container and send log files")

try:
    if (result['exit_code'] == "0"):
        print("Logs successfully sent.")
        remove_container("filebeat")
    else:
        print("Something went wrong!")
        rename_container("filebeat", "filebeat_" + TIMESTAMP)
except:
    print("Could not remove/rename container")
    exit(1)
