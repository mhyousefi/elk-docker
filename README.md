# elk-docker
A docker-compose setup for running the popular image sebp/elk as well as the official Filebeat image

## How it works
There are two main directories: `elk` and `filebeat`, each containing a `docker-compose.yml` along with other files to run the sebp/elk and the official filebeat images respectively. Therefore, the filebeat container is seperate from the elk one. 

## How to use it
#### 1. Without Filebeat:
- Run `docker-compose -f ${repo_dir}/elk/docker-compose.yml up` (from any directories) in the terminal. 
- Then wait for the log line `elk_1 | {"type":"log","@timestamp":"2018-08-12T08:30:27Z","tags":["listening","info"],"pid":247,"message":"Server running at http://0.0.0.0:5601"}` and you are good to go. At this point, the `Logstash` config file at `${repo_dir}/elk/volumed-folder/config` has been applied and you should interact with `Logstash` as expected.

#### 2. With Filebeat:
- As with the first case, you need to run the `docker-compose -f ${repo_dir}/elk/docker-compose.yml up` first to create the elk container. **IMPORTANT:** before running the command, make sure a suitable `Logstash` config file (which listens on port 5044 for incoming beats inputs) is the only file at `${repo_dir}/elk/volumed-folder/config`.
- To create the `Filebeat` container, you need to run the Python script at `${repo_dir}/filebeat/scripts/filebeat.py`. The command should look like this: `python3 ${repo_dir}/filebeat/scripts/filebeat.py data_file_abs_path index_pattern` Where the two arguments passed are:
  1. `data_file_abs_path`: an absolute path to the file you want `Filebeat` to send to `Logstash`.
  2. `index_pattern`: an index pattern


**NOTE**: The logstash inside the elk container is watching the container's internal directory at `/etc/logstash/conf.d` for config files. The elk `docker-compose.yml` mounts the `${repo_dir}/elk/volumed-folder/config` directory onto the mentioned internal directory. There are initially three config files at `${repo_dir}/elk/volumed-folder/config`: 
* `txt-config.conf`: this config feeds the txt files at `/logstash/data/` to Elasticsearch.
* `csv-config.conf`: this config feeds the csv files at `/logstash/data/` to Elasticsearch.
* `filebeat-config.conf`: this config has the logstash listen on the container's internal 5044 port for incoming `Filebeat` inputs and sends them over to Elasticsearch.

**I HIGHLY RECOMMEND THAT YOU HAVE ONLY ONE CONFIG FILE AT `${repo_dir}/elk/volumed-folder/config`.** Although, having multiple files will still work, and `Kibana` will create indecies, I have witnessed irregular behaviors when more than one config files are given to the container.

Feel free to put your own custom config file for `Logstash` at `${repo_dir}/elk/volumed-folder/config` before creating the elk container. [This](https://www.elastic.co/guide/en/logstash/6.2/config-examples.html) is a good link from Logstash documentation, which includes suitable examples of complex Logstash config files.
