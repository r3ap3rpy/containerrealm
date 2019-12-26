### This guide gets you setup witht the ELKF stack

We would like to collect logs from our containers, that allow us to take actions based on utilization.

## Installing [Elasiticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/rpm.html)

You need to edit the **/etc/yum.repos.d/elk.repo** file

Add the below lines.

``` bash
[elasticsearch]
name=Elasticsearch repository for 7.x packages
baseurl=https://artifacts.elastic.co/packages/7.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
```

Then issue the following command.

``` bash
sudo yum install elasticsearch -y
```

Now we need to configure the service.

Under the **/etc/elasticsearch/elasticsearch.yml** file we want these lines to be present.

``` bash
network.host: 127.0.0.1
http.host: 0.0.0.0
http.port: 9200
```

Now we can enable and start the service.

``` bash
sudo systemctl enable elasticsearch
sudo systemctl start elasticsearch
```

## Installing [Kibana](https://www.elastic.co/guide/en/kibana/current/rpm.html)

The same repository provides the packages as the one for the elasticsearch.

If you already have setup the repository you have nothing to do.

Issue the install command.

``` bash
sudo yum install kibana -y 
```

Now once the install is complete you need to enable and start the service.

## Installing [Fluentd](https://docs.fluentd.org/installation/install-by-rpm)

We do not need to  prepare anything in advance.

``` bash
curl -L https://toolbelt.treasuredata.com/sh/install-redhat-td-agent3.sh | sh
```

Once the install is complete we need to enable and start the service.

``` bash
sudo systemctl enable td-agent
sudo systemctl start td-agent
```

Remember, every modification to the **/etc/td-agent/td-agent.conf** needs a service restart.

After restart you can live check what logs are forwarded and processerd under this file: **/var/log/td-agent/td-agent.log**

Let's modify our configuration.

``` bash
<source>                                       
  @type forward                                
  port 24224                                   
  bind 0.0.0.0                                 
  tag docker.*                                 
</source>                                      
<match docker.*>                               
  @type stdout                                 
</match>                                       
                                               
<filter docker.**>                             
  @type parser                                 
  format json # apache2, nginx, etc...         
  key_name log                                 
  reserve_data true                            
</filter>                                      
                                               
<match docker.*>                               
  @type elasticsearch                          
  host centosd                                 
  port 9200                                    
  logstash_format true                         
  index_name fluentd                           
</match>
```                                       

Now just restart the service.

``` bash
systemctl restart td-agent
```

When we start up a docker container we should add the following arguments.

``` bash
docker run -d --log-driver=fluentd --log-opt tag="docker.{.ID}" <container>
```

This will become visible to our kibana web ui, and the logs will show something like this.

``` bash
[root@centosa ~]# tailf  /var/log/td-agent/td-agent.log
2019-12-26 21:28:46 +0100 [info]: gem 'fluentd' version '1.7.4'
2019-12-26 21:28:46 +0100 [info]: adding match pattern="docker.*" type="stdout"
2019-12-26 21:28:46 +0100 [info]: adding filter pattern="docker.**" type="parser"
2019-12-26 21:28:46 +0100 [info]: adding match pattern="docker.*" type="elasticsearch"
2019-12-26 21:28:46 +0100 [warn]: #0 Detected ES 7.x or above: `_doc` will be used as the document `_type`.
2019-12-26 21:28:46 +0100 [warn]: #0 To prevent events traffic jam, you should specify 2 or more 'flush_thread_count'.
2019-12-26 21:28:46 +0100 [info]: adding source type="forward"
2019-12-26 21:28:46 +0100 [info]: #0 starting fluentd worker pid=8527 ppid=8522 worker=0
2019-12-26 21:28:46 +0100 [info]: #0 listening port port=24224 bind="0.0.0.0"
2019-12-26 21:28:46 +0100 [info]: #0 fluentd worker is now running worker=0
^[[A2019-12-26 21:29:12.000000000 +0100 docker.*: {"source":"stdout","log":" * Serving Flask app \"App\" (lazy loading)","container_id":"587623f8beb6636251457fb846dc13e940edb96cf34d905bc34998383ecd30ce","container_name":"/compassionate_dewdney"}
2019-12-26 21:29:12.000000000 +0100 docker.*: {"container_id":"587623f8beb6636251457fb846dc13e940edb96cf34d905bc34998383ecd30ce","container_name":"/compassionate_dewdney","source":"stdout","log":" * Environment: production"}
2019-12-26 21:29:12.000000000 +0100 docker.*: {"container_id":"587623f8beb6636251457fb846dc13e940edb96cf34d905bc34998383ecd30ce","container_name":"/compassionate_dewdney","source":"stdout","log":"   WARNING: This is a development server. Do not use it in a production deployment."}
2019-12-26 21:29:12.000000000 +0100 docker.*: {"container_id":"587623f8beb6636251457fb846dc13e940edb96cf34d905bc34998383ecd30ce","container_name":"/compassionate_dewdney","source":"stdout","log":"   Use a production WSGI server instead."}
2019-12-26 21:29:12.000000000 +0100 docker.*: {"container_id":"587623f8beb6636251457fb846dc13e940edb96cf34d905bc34998383ecd30ce","container_name":"/compassionate_dewdney","source":"stdout","log":" * Debug mode: on"}
```