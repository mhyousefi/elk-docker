from utils import exec_bash_command


def docker_compose_up(docker_compose_addr):
    command = "docker-compose -f {0} up".format(docker_compose_addr)
    return exec_bash_command(command)

def remove_container(name):
    return exec_bash_command("docker rm " + name)

def rename_container(old_name, new_name):
    command = "docker rename {0} {1}".format(old_name, new_name)
    return exec_bash_command(command)
