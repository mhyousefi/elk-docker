from utils import get_relative_path


INPUT_LINES = [
    'filebeat.inputs:\n',
    '- type: log\n',
    '  enabled: true\n',
    '  close_eof: true\n',
    '  paths:\n',
    '    - ${PWD}/filebeat-volume/data/*.txt\n'
]

LOGSTASH_LINES = [
    'output.logstash:\n',
    '  enabled: true\n',
    '  hosts: ["elk:5044"]\n',
]

KIBANA_LINES = [
    'setup.kibana:\n',
    '  host: "localhost:5601"\n',
]

def create_input_str():
    res = ''.join(INPUT_LINES) + '\n'
    return res

def create_logstash_str(index_pattern):
    res = ''.join(LOGSTASH_LINES)
    res += '  index: "{0}"'.format(index_pattern) + '\n\n'
    return res

def create_kibana():
    return ''.join(KIBANA_LINES)

def create_filebeat_config(timestamp, index_pattern):
    file_dir = get_relative_path('../call-history/{0}/filebeat.yml'.format(timestamp))
    conf_file = open(file_dir, 'w')
    conf_file.write(create_input_str())
    conf_file.write(create_logstash_str(index_pattern))
    conf_file.write(create_kibana())
    conf_file.close()
