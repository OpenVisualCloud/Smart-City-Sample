The sample can be deployed with either docker-compose (v1.20+ required) or docker swarm. The deployment uses the same configuration script.   

### Docker-Compose Deployment

This is as simple as 

```
make start_docker_compose
make stop_docker_compose
```

If you setup more than 1 office, please follow the [instructions](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/vm-max-map-count.html) to increase the VM mapping threshold.

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
  - Create a user of the same user id (uid) and group id (gid) as the current user of the manager node.      
  - Follow the [instructions](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/vm-max-map-count.html) to increase the VM mapping threshold.    

- On the swarm manager, label each swarm node as follows:    
  - Label the nodes where office services must run, for example, ```office1_zone=yes```, ```office2_zone=yes```, ```office3_zone=yes```, etc. You can label multiple machines under the same office zone so that the workloads can be distributed.  
  - Each office must designate a node that handles the recording storage (storage space needed). Label the nodes as ```office1_storage=yes```, ```office2_storage=yes```, ```office3_storage=yes```, etc.

```
sudo docker node update --label-add office1_zone=yes <swarm-node>
sudo docker node update --label-add office1_storage=yes <swarm-node>
```

- On the swarm manager, setup password-less acess from the swarm manager to each swarm node:   

```
ssh-keygen
ssh-copy-id <worker>
```

Finally, start/stop services as follows:   

```
make update      # distribute images to swarm nodes
make start_docker_swarm
make stop_docker_swarm
```

### See Also 

- [Utility Scripts](../../doc/script.md)   

