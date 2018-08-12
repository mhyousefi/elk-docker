# elk-docker
A docker-compose setup for running the popular image sebp/elk

### How to use it
* After cloning the repository, **make sure to change `/path/to/logstash/folder` in docker-compose.yml to a valid directory path!**
* Move to the local repository directory and run the command `docker-compose up elk` and wait for the following log: `elk_1  | {"type":"log","@timestamp":"2018-08-12T08:30:27Z","tags":["listening","info"],"pid":247,"message":"Server running at http://0.0.0.0:5601"}`.
* Open another terminal tab and run `docker exec -it <container-name> bash`. Once in the container terminal, you have two options for starting logstash:
  1. **`simple-config.conf`**: run `/opt/logstash/bin/logstash --path.data /tmp/logstash/data -f /logstash/config/simple-config.conf`. This config just receives messages from the container terminal stdin and dumps them to elasticsearch.
  2. **`file-config.conf`**: run `/opt/logstash/bin/logstash --path.data /tmp/logstash/data -f /logstash/config/file-config.conf`. This config feeds the file `/logstash/data/random-data.csv` to elasticsearch.
  
You could look through my `/logstash` directory and change the files to suit your specific needs.

`https://www.elastic.co/guide/en/logstash/6.2/config-examples.html` is a good link from Logstash documentation, which includes suitable examples of complex Logstash config files.
