The E2E sample implements aspects of smart city sensing, analytics and management features as follows:   

<IMG src="doc/scope.png" height="250px">

- **Camera Provisioning**: Tag and calibrate cameras for installation locations, calibration parameters and other usage pattern information.   
- **Camera Discovery**: Discover and register IP cameras on specified IP blocks. Registered cameras automatically participate into the analytics activities. See [Sensor Simulation and Discovery](sensor/README.md) for additional details.    
- **Recording**: Record and manage segmented camera footage for preview or review (at a later time) purpose.     
- **Analytics**: Perform analytics on the live/recorded camera streams. Latency-sensitive analytics are performed on Edge while others are on cloud.     
- **Triggers and Alerts**: Manage triggers on analytics data. Respond with actions on triggered alerts.   
- **Smart Upload and Archive**: Transcode and upload only critical data to cloud for archival or further offline analysis.    
- **Stats**: Calculate statistics for planning/monitoring purpose on analytical data.    
- **UI**: Present above data to users/administrators/city planners.     

The sample showcases the following pipeline operations using the Open Visual Cloud software stacks:      
- **Edge Low-latency Analytics**:   

<IMG src="doc/edge-analytics-arch.png" height="200px">

- **Smart Upload with Transcoding**:

<IMG src="doc/smart-upload-arch.png" height="180px">

The following diagram illustrates how the sample is constructed: a set of services each retrieves the work order by querying the database and submits the processing results back into the database. See also: [Content Search](doc/search.md).          

<IMG src="doc/data-centric-design.png" height="400px">

### Prerequisites

- **Time Zone**: Check that the timezone setting of your host machine is correctly configured. Timezone is used during build. If you plan to run the sample on a cluster of machines managed by Docker Swarm or Kubernetes, please make sure to synchronize time among the manager node and worker nodes.    

- **Build Tools**: Install ```cmake``` and ```m4``` if they are not available on your system.        

- **Docker Engine**:        
  - Install [docker engine](https://docs.docker.com/install).     
  - Install [docker compose](https://docs.docker.com/compose/install), if you plan to deploy through docker compose. Version 1.20+ is required.    
  - Setup [docker swarm](https://docs.docker.com/engine/swarm), if you plan to deploy through docker swarm. See [Docker Swarm Setup](deployment/docker-swarm/README.md) for additional setup details.  
  - Setup [Kubernetes](https://kubernetes.io/docs/setup), if you plan to deploy through Kubernetes. See [Kubernetes Setup](deployment/kubernetes/README.md) for additional setup details.     
  - Setup docker proxy as follows if you are behind a firewall:   

```bash
sudo mkdir -p /etc/systemd/system/docker.service.d       
printf "[Service]\nEnvironment=\"HTTPS_PROXY=$https_proxy\" \"NO_PROXY=$no_proxy\"\n" | sudo tee /etc/systemd/system/docker.service.d/proxy.conf       
sudo systemctl daemon-reload          
sudo systemctl restart docker     
```

### Build Sample: 

```bash
mkdir build    
cd build     
cmake ..    
make     
```

See also: [Customize Build Process](doc/cmake.md).    

### Start/stop Sample: 

Use the following commands to start/stop services via docker-compose:        

```bash
make start_docker_compose      
make stop_docker_compose      
```

Use the following commands to start/stop services via docker swarm:    

```bash
make update
make start_docker_swarm      
make stop_docker_swarm      
```

See also:  [Docker Swarm Setup](deployment/docker-swarm/README.md).    

Use the following commands to start/stop Kubernetes services:

```
make update
make start_kubernetes
make stop_kubernetes
```

See also: [Kubernetes Setup](deployment/kubernetes/README.md).    

### Launch Sample UI:

Launch your browser and browse to ```https://<hostname>```. You should see something similar to the following UI:   

<IMG src="doc/screenshot.git" height="270px"></IMG>

---

* For Kubernetes/Docker Swarm, ```<hostname>``` is the hostname of the master node.
* If you see a browser warning of self-signed certificate, please accept it to proceed to the sample UI.    
  
---

### See Also

- [Configuration Options](doc/cmake.md)          
- [Docker Swarm Setup](deployment/docker-swarm/README.md)      
- [Kubernetes Setup](deployment/kubernetes/README.md)
- [Intel VCAC-A Setup](doc/vcac-a.md)
- [Sensor Simulation and Discovery](sensor/README.md)  
- [Search Capabilities](doc/search.md)       
- [Extending Offices, Sensors and Maps](doc/extend.md)  
- [Utility Scripts](doc/script.md)       

