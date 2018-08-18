import os


my_path = os.path.abspath(os.path.dirname(__file__))

COMPOSE_LINES_BEFORE_VOLUME_PATH = [
    'version: "2"\n',
    '\n', 'services:\n',
    '  filebeat:\n',
    '    container_name: filebeat\n',
    '    hostname: filebeat\n',
    '    image: docker.elastic.co/beats/filebeat:6.3.0\n',
    '    user: root\n',
    '    command: bash -c \'cd /usr/share/filebeat && rm filebeat.yml && cp filebeat-volume/filebeat.yml . && ./filebeat --once -e -c filebeat.yml -d "*"\'\n',
    '    volumes:\n',
]

COMPOSE_LINES_AFTER_VOLUME_PATH = [
    '    networks:\n',
    '      - filebeat_net\n',
    '\n',
    'networks:\n',
    '  filebeat_net:\n',
    '    external:\n',
    '      name: elk_elk_net\n'
]

def create_docker_compose(timestamp):
    docker_compose_file = open('../call-history/{0}/docker-compose.yml'.format(timestamp), 'w')
    docker_compose_file.write(''.join(COMPOSE_LINES_BEFORE_VOLUME_PATH))
    host_path = os.path.join(my_path, "../call-history/{0}".format(timestamp))
    volume_path_line = '      - {0}:/usr/share/filebeat/filebeat-volume\n'.format(host_path)
    docker_compose_file.write(volume_path_line)
    docker_compose_file.write(''.join(COMPOSE_LINES_AFTER_VOLUME_PATH))
    docker_compose_file.close()
