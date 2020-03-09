
### Deploying Smart City Sample under Open Network Edge Services Software (OpenNESS)

The set of scripts deploy the Smart City sample under OpenNESS. Different from development, where all containers deploy to a single machine or a swarm of machines, the OpenNESS deployment requires that the containers be deployed to different networks in the cloud, on the edge and around the cameras. 

Deployment sequence:
```
make start_openness_camera
make start_openness_cloud
make start_openness_office
```

```
make stop_openness_cloud
make stop_openness_office
make stop_openness_camera
```

### Setup Simulated Cameras

The machine used for camera simulation does not need to be in a Kubernetes or docker swarm cluster, it can be a single machine with docker installed. Assuming that we are going to run 3 offices and 5 cameras per office, run the following commands on each machine to simulate cameras for each office, 

```
cmake -DNOFFICES=3 -DNCAMERAS=5 ..
make start_openness_camera
```

### Setup Cloud Machine

Cloud will be running in a Kubernetes cluster which consists of one master node and one worker node. The Smart City sample will setup ssh tunnels between offices and cloud for database cluster transport and office storage access. 

On both 2 nodes, run the following commands

```
1. sudo vi /etc/ssh/sshd_config
2. change "GatewayPorts yes"
3. sudo service ssh restart
```

You will need to label the worker node
```
kubectl label node <worker-node> cloud-zone=yes
kubectl label node <worker-node> cloud-storage=yes
```

To start the cloud, run the followings

```
cmake -DNOFFICES=3 -DNCAMERAS=5 ..
make start_openness_cloud
```

### Setup Office Machines

Offices will be running in a Kubernetes cluster which consists of one master node and several worker nodes. Each office runs on a single worker node. You will need to label the node for each offices. For example, for office1, login to the node and run the followings

```
kubectl label node <worker-node> office1-zone=yes
kubectl label node <worker-node> office1-storage=yes
```

To start the offices, on master node, run the followings

```
cmake -DNOFFICES=3 -DNCAMERAS=5 -DNANALYTICS=5 ..

export CAMERA_HOSTS=ip-of-camera-host1,ip-of-camera-host2,ip-of-camera-host3
export CLOUD_HOST=cloud-master-node-ip
make start_openness_office
```
