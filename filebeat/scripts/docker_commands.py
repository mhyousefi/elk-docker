from utils import exec_bash_command


EXPECTED_SUCCESS_LOGS = [
    "End of file reached",
    "Registry file updated",
    "harvester cleanup finished for file",
    "message",
    "All data collection completed. Shutting down.",
    "Loading and starting Inputs completed"
]

def docker_compose_up(docker_compose_addr):
    command = "docker-compose -f {0} up".format(docker_compose_addr)
    return exec_bash_command(command, show_logs=True)

def filebeat_was_successful(result):
    if (result["exit_code"] != "0"):
        print ("Exit code was not 0!")
        return False

    for log in EXPECTED_SUCCESS_LOGS:
        if log not in result["stdout"]:
            print("Stdout logs don't match a sucessful case!")
            return False

    return True

def remove_container(name):
    return exec_bash_command("docker rm " + name)

def rename_container(old_name, new_name):
    command = "docker rename {0} {1}".format(old_name, new_name)
    return exec_bash_command(command)
