The sample can be deployed with either docker-compose (v1.20+ required) or docker swarm. The deployment uses the same configuration script.   

### Docker-Compose Deployment

This is as simple as 
```
make start_docker_compose
make stop_docker_compose
```

### Docker Swam Single Machine Deployment

Initialize docker swarm if you have not:
```
sudo docker swarm init
```
Then start/stop services as follows:
```
make start_docker_swarm
make stop_docker_swarm
```

### Docker Swam Multiple Nodes Deployment

Follow the [instructions](https://docs.docker.com/engine/swarm/swarm-tutorial/create-swarm) to create a swarm. Then setup the swarm as follows:     
- On each swarm node, 
  - Create a user of the same user id (uid) and group id (gid) as the current user on the manager node.      
  - Follow the [instructions](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/vm-max-map-count.html) to increase the VM mapping threshold.    
- Label each swarm node as follows:    
  - For each office, label the nodes where office services must run, for example, ```office1_zone=yes```, ```office2_zone=yes```, ```office3_zone=yes```, etc. You can label multiple machines under the same office zone so that the workloads can be distributed.     
  - For each office, designate a single node for the recording storage with label ```office1_storage=yes```, ```office2_storage=yes```, ```office3_storage=yes```, etc. Create the ```/mnt/storage``` directory for the recording storage and set the read/write permission. Alternatively, you could also designate the storage to be on multiple machines shared via NFS.     
- Use the [update-image.sh](../../script/update-image.sh) script to update/upload the docker images to each swarm node.    

Finally, start/stop services as follows:   

```
make start_docker_swarm
make stop_docker_swarm
```

The recordings are stored under ```/mnt/storage``` on each swarm node labeled ```office?_storage```. You can run the [clean-storage.sh](../../script/clean-storage.sh) script to clean up the recording data.   

See also [utility scripts](../../doc/script.md).   

