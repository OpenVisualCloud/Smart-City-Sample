
The sample provides utility scripts (under the [script](../script) folder) to facilitate sample development and deployment:   

### [backup-image.sh](../script/backup-image.sh)

The script scans the generated ```docker-compose.yml``` of a specific deployment, and archives the used docker images. To use the script, first perform a normal build ```cmake...make...``` and then run the backup script. The script does not take any command-line argument. The archived tar files are saved under the ```archive``` directory at the sample project root.   

### [restore-image.sh](../script/restore-image.sh)

The script restores the saved docker images to the current host. The script does not take any command-line argument.     

### [update-image.sh](../script/update-image.sh)

The script updates the docker swarm nodes with the most recent images (on the current host.) The script scans the generated ```docker-compose.yml``` of a specific deployment, and checks the swarm worker nodes to ensure that they have the most recent images. If any node got out-dated images, the script updates them.    

To use the script, first perform a normal build ```cmake...make...``` and then run the update script. The script does not take any command-line argument.    

The script assumes there is password-less access between the swarm manager and the swarm workers. You can setup as follows:     

```
ssh-keygen
ssh-copy-id <worker>
```

### [clean-storage.sh](../script/clean-storage.sh)

The script cleans the ```/mnt/storage``` directory on each swarm node. There is no command-line argument.    

