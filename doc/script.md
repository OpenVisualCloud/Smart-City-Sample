
The sample provides utility scripts (under the [script](../script) folder) to facilitate sample development and deployment:   

---
Password-less access is assumed between the swarm manager and the workers. Setup as follows on each worker node:     
```
ssh-keygen
ssh-copy-id <worker>
```
---

### [mk-dist.sh](../script/mk-dist.sh)

The script creates a sample distribution package that contains sample (docker) images, deployment scripts and media files under the `dist` directory. You can [distribute the sample](dist.md) to a different system for evaluation and demonstration without the need to rebuild the sample.  

### [update-image.sh](../script/update-image.sh)

The script updates the docker swarm nodes with the most recent images (on the current host.) The script scans the generated ```docker-compose.yml``` of a specific deployment, and checks the swarm worker nodes to ensure that they have the most recent images. If any node got out-dated images, the script updates them.    

To use the script, first perform a normal build ```cmake...make...``` and then run the update script. The script does not take any command-line argument.    

### [cleanup.sh](../script/cleanup.sh)

The script cleans up unused volumes, containers and networks on each docker swarm node. The script is called everytime you start docker swarm. There is no command line argument.    

