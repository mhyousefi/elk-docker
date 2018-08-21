import sys
from utils import *
from docker_commands import *
from docker_compose_config import create_docker_compose
from filebeat_config import create_filebeat_config


def create_call_folder(timestamp, data_file_path, index):
    call_history_dir = "${repo_dir}/filebeat/call-history/" + timestamp

    if create_call_history_folder().returncode != 0:
        raise RuntimeError("Failed to execute mkdir -p {0}.".format(call_history_dir))

    if create_call_dir(timestamp).returncode != 0:
        raise RuntimeError("Failed to create {0}".format(call_history_dir))
    print("====> Created directory {0}.".format(call_history_dir))

    try:
        create_docker_compose(timestamp)
        print("====> Craeted docker-compose.yml at {0}.".format(call_history_dir))
    except Exception as e:
        raise RuntimeError(str(e))

    try:
        create_filebeat_config(timestamp, index)
        print("====> Created filebeat.yml at {0}.".format(call_history_dir))
    except Exception as e:
        raise RuntimeError(str(e))

    if move_txt_file(timestamp, data_file_path).returncode != 0:
        raise RuntimeError("Failed to move file at {0} to {1}".format(data_file_path, call_history_dir))
    print("====> Moved {0} to {1}".format(data_file_path, call_history_dir) + "\n\n")

try:
    DATA_FILE_PATH = sys.argv[1]
    INDEX = sys.argv[2]
    TIMESTAMP = get_date_time()
    DOCKER_COMPOSE_ADDR = get_relative_path("../call-history/{0}/docker-compose.yml".format(TIMESTAMP))
except Exception as e:
    print("Invalid arguments!")
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
