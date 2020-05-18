
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

- Optional: on the swarm manager, setup password-less acess from the swarm manager to each swarm node (required by `make update`):   

```
ssh-keygen
ssh-copy-id <worker>
```

Finally, start/stop services as follows:   

```
make update # optional for private registry
make start_docker_swarm
make stop_docker_swarm
```

---

The command `make update` uploads the sample images to each worker node. If you prefer to use a private docker registry, configure the sample, `cmake -DREGISTRY=<registry-url> ..`, to push images to the private registry after each build.  

---

### See Also 

- [Utility Scripts](../../doc/script.md)   
- [CMake Options](../../doc/cmake.md)   
- [Intel VCAC-A Setup](../../doc/vcac-a.md)    

