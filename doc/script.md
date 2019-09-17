
The sample provides utility scripts (under the [script](../script) folder) to facilitate sample development and deployment:   

---
Password-less access is assumed between the swarm manager and the workers. Setup as follows on each worker node:     
```
ssh-keygen
ssh-copy-id <worker>
```
---

### [backup-image.sh](../script/backup-image.sh)

The script scans the generated ```docker-compose.yml``` of a specific deployment, and archives the used docker images. To use the script, first perform a normal build ```cmake...make...``` and then run the backup script. The script does not take any command-line argument. The archived tar files are saved under the ```archive``` directory at the sample project root.   

### [restore-image.sh](../script/restore-image.sh)

The script restores the saved docker images to the current host. The script does not take any command-line argument.     

### [update-image.sh](../script/update-image.sh)

The script updates the docker swarm nodes with the most recent images (on the current host.) The script scans the generated ```docker-compose.yml``` of a specific deployment, and checks the swarm worker nodes to ensure that they have the most recent images. If any node got out-dated images, the script updates them.    

To use the script, first perform a normal build ```cmake...make...``` and then run the update script. The script does not take any command-line argument.    

### [cleanup.sh](../script/cleanup.sh)

The script cleans up unused volumes, containers and networks on each docker swarm node. The script is called everytime you start docker swarm. There is no command line argument.    
