The sample can be deployed with either docker-compose (v1.20+ required) or docker swarm. The deployment uses the same configuration script.   

### Docker-Compose Deployment

This is as simple as 

```
make start_docker_compose
make stop_docker_compose
```

If you setup more than 1 office, please follow the [instructions](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/vm-max-map-count.html) to increase the VM mapping threshold.

### Docker Swam Single Office Deployment

Initialize docker swarm if you have not:
```
sudo docker swarm init
```
Then start/stop services as follows:
```
make start_docker_swarm
make stop_docker_swarm
```

### Docker Swam Multiple-Office/Node Deployment

Follow the [instructions](https://docs.docker.com/engine/swarm/swarm-tutorial/create-swarm) to create a swarm. Then setup the swarm as follows:     

- On each swarm node, 
  - Create a user of the same user id (uid) and group id (gid) as the current user of the manager node.      
  - Follow the [instructions](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/vm-max-map-count.html) to increase the VM mapping threshold.    

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
- [CMake Options](../../doc/cmake.md)   
- [Intel VCAC-A Setup](../../doc/vcac-a.md)    


