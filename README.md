
# elk-docker
A docker-compose setup for running the `ELK stack` and `Filebaet` using the popular image [sebp/elk](https://hub.docker.com/r/sebp/elk/) as well as the [official Filebeat image](https://www.elastic.co/guide/en/beats/filebeat/current/running-on-docker.html)

## How to use it
#### 1. Without Filebeat:
1. Run `docker-compose -f ${repo_dir}/elk/docker-compose.yml up` (from any directory) in your terminal. 
2. Then wait for the line containing `"Server running at http://0.0.0.0:5601"` and you are good to go. At this point, the Logstash config files at `${repo_dir}/elk/volumed-folder/config` have been applied and you should interact with Logstash as expected. _(Please read the **IMPORTANT NOTE** bellow regarding Logstash config files)_

#### 2. With Filebeat:
1. As with the first case, you first need to run the `docker-compose -f ${repo_dir}/elk/docker-compose.yml up`  to create the elk container. **IMPORTANT:** before running the command, make sure a suitable Logstash config file (which listens on port 5044 for incoming beats inputs) is present at `${repo_dir}/elk/volumed-folder/config`.
2. To create the Filebeat container, you need to run the Python script named `filebeat.py`. The command should look like this: `python3 ${repo_dir}/filebeat/scripts/filebeat.py data_file_abs_path index_name`. The two arguments passed are:
   1. `data_file_abs_path`: an absolute path to the file you want Filebeat to send to Logstash.
   2. `index_name`: an index name to be used by Elasticsearch.
 
## How it works
There are two main directories: `elk` and `filebeat` in the repository's root, each containing a `docker-compose.yml` along with other files to create the sebp/elk and the official filebeat containers respectively. *Therefore, the filebeat container is seperate from the elk one.*

### The ELK contianer
The Logstash instance inside the elk container is watching the container's internal directory at `/etc/logstash/conf.d` for config files. The elk `docker-compose.yml` mounts the `${repo_dir}/elk/volumed-folder/config` directory onto the mentioned internal directory. There are initially three config files at `${repo_dir}/elk/volumed-folder/config`: 
* `txt-config.conf`: this config feeds the txt files at `/logstash/data/` to Elasticsearch.
* `csv-config.conf`: this config feeds the csv files at `/logstash/data/` to Elasticsearch.
* `filebeat-config.conf`: this config has the logstash listen on the container's internal 5044 port for incoming Filebeat inputs and sends them over to Elasticsearch.

Feel free to put your own custom config file for `Logstash` at `${repo_dir}/elk/volumed-folder/config` before creating the elk container. [This](https://www.elastic.co/guide/en/logstash/6.2/config-examples.html) is a good link from Logstash documentation, which includes suitable examples of complex Logstash config files.

  #### IMPORTANT NOTE:
  I highly recommend that you have **ONLY ONE CONFIG FILE** at `${repo_dir}/elk/volumed-folder/config`. Although, having multiple files will still work and Elasticsearch will create indecies, I have witnessed irregular behaviors when more than one config files are given to the container.
  
### The Filebeat contianer
The script, `filebeat.py`   does three things:
1. Creates the directory `${repo_dir}/filebeat/call-history/${script_call_timestamp}` containing a `docker-compose.yml`, `filebeat.yml`, and a folder called `data` containing the file whose path was given to the script (the file is moved here).
2. Executes the command `docker-compose -f ${repo_dir}/filebeat/call-history/${script_call_timestamp}/docker-compose.yml up` to create a container from the official `Filebeat` container. The `${repo_dir}/filebeat/call-history` directory is included in `.gitignore`.
3. Checks whether the logs were sent and:
   * If successful, the container is **removed**.
   * Otherwise, the container name is changed to `Filebeat_${script_call_timestamp}`.
