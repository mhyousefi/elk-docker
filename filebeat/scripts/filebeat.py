import sys
from utils import get_date_time, exec_bash_command, create_call_dir, move_txt_file, get_relative_path
from docker_commands import docker_compose_up, remove_container, rename_container, filebeat_was_successful
from docker_compose_config import create_docker_compose
from filebeat_config import create_filebeat_config


def create_call_folder(timestamp, data_file_path, index):
    call_history_path = get_relative_path('../call-history')
    exec_bash_command("mkdir -p " + call_history_path)
    create_call_dir(timestamp)
    create_docker_compose(timestamp)
    create_filebeat_config(timestamp, index)
    move_txt_file(timestamp, data_file_path)

try:
    DATA_FILE_PATH = sys.argv[1]
    INDEX = sys.argv[2]
    TIMESTAMP = get_date_time()
    DOCKER_COMPOSE_ADDR = get_relative_path("../call-history/{0}/docker-compose.yml".format(TIMESTAMP))
except Exception as e:
    print("No arguments passed")
    print("ERROR MESSAGE => {0}".format(str(e)))
    exit(1)

try:
    create_call_folder(TIMESTAMP, DATA_FILE_PATH, INDEX)
except Exception as e:
    print("Could not create the call folder")
    print("ERROR MESSAGE => {0}".format(str(e)))
    exit(1)

try:
    result = docker_compose_up(DOCKER_COMPOSE_ADDR)
except Exception as e:
    print("Could not create container and send log files")
    print("ERROR MESSAGE => {0}".format(str(e)))
    exit(1)

try:
    if (filebeat_was_successful(result)):
        print("Logs successfully sent! Deleting the container...")
        remove_container("filebeat")
    else:
        new_container_name = "filebeat_" + TIMESTAMP
        print("Renaming the container to {0}...".format(new_container_name))
        rename_container("filebeat", new_container_name)
except Exception as e:
    print("Could not remove/rename container")
    print("ERROR MESSAGE => {0}".format(str(e)))
    exit(1)
