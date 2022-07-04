
The Smart-City sample implements aspects of smart city sensing, analytics and management features as follows:   

- **Camera Provisioning**: Tag and calibrate cameras for installation locations, calibration parameters and other usage pattern information.   
- **Camera Discovery**: Discover and register IP cameras on specified IP blocks. Registered cameras automatically participate into the analytics activities.  
- **Recording**: Record and manage segmented camera footage for preview or review (at a later time) purpose.  
- **Analytics**: Perform analytics on the live/recorded camera streams. Latency-sensitive analytics are performed on Edge while others are on cloud.     
- **Triggers and Alerts**: Manage triggers on analytics data. Respond with actions on triggered alerts.   
- **Smart Upload and Archive**: Transcode and upload only critical data to cloud for archival or further offline analysis.    
- **Stats**: Calculate statistics for planning/monitoring purpose on analytical data.    
- **UI**: Present above data to users/administrators/city planners.   

### Scenarios

The sample implements the Smart-City `traffic` and `stadium` scenarios. The `traffic` scenario measures vehicle/pedestrian flow for planning purpose. The `stadium` scenario focuses on different access control techniques, including entrance people counting, service-point queue counting, and stadium seating zone crowd counting.   

### Software Stacks

The sample is powered by the following Open Visual Cloud software stacks:      
- **Edge Low-latency Analytics**:   
  - [The GStreamer-based media analytics stack](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/Xeon/ubuntu-18.04/analytics/gst) is used for object detection, people-counting, queue-counting and crowd-counting on camera streams. The software stack is optimized for [Intel® Xeon® Scalable Processors](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/Xeon/ubuntu-18.04/analytics/gst) and [Intel VCAC-A](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/VCAC-A/ubuntu-18.04/analytics/gst).  
 
- **Smart Upload with Transcoding**:
  - [The FFmpeg-based media transcoding stack](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/Xeon/ubuntu-20.04/media/ffmpeg) is used to transcode recorded content before uploading to cloud. The software stack is optimized for [Intel Xeon Scalable Processors](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/Xeon/ubuntu-20.04/media/ffmpeg).  

### Install Prerequisites:

- **Time Zone**: Check that the timezone setting of your host machine is correctly configured. Timezone is used during build. If you plan to run the sample on a cluster of machines managed by Docker Swarm or Kubernetes, please make sure to synchronize time among the manager/master node and worker nodes.    

- **Build Tools**: Install `cmake` and `m4` if they are not available on your system.        

- **Orchestration**:         
  - Install [docker](../../docker-swarm/setup-docker.md).    
  - Setup [Kubernetes](../setup-kubernetes.md).  

### Build Sample: 

Use the following commands to build the sample. By default, the sample builds to the `traffic` scenario. To enable the `stadium` scenario, use `cmake -DSCENARIO=stadium ..`.  

```bash
mkdir build    
cd build     
cmake ..    
make     
```

### Start/stop Sample: 

Use the following commands to start/stop Kubernetes services:

```
make update # optional for private registry
make start_helm
make stop_helm
```

---

The command `make update` uploads the sample images to each worker node. If you prefer to use a private docker registry, configure the sample, `cmake -DREGISTRY=<registry-url>, to push images to the private registry during each build.  

---

### Launch Sample UI:

Launch your browser and browse to `https://<hostname>` for the sample UI. 

---

* `<hostname>` is the hostname of the manager/master node.
* If you see a browser warning of self-signed certificate, please accept it to proceed to the sample UI.    
  
---

### Multiple Office Start/Stop  

The sample supposes dynamic office starting/stopping. It supports the IP cameras deployed in the gateway and pushed to office via gb28181. You can selectively start and stop any office, as follows:

```
cmake -DNOFFICES=2 ..
make

SCOPE=cloud make start_helm
SCOPE=office1 make start_helm
SCOPE=office2 make start_helm
...
SCOPE=office1 make stop_helm
...
SCOPE=office1 make start_helm
...
SCOPE=office1 make stop_helm
SCOPE=office2 make stop_helm
SCOPE=cloud make stop_helm
```

### Multiple Office Start/Stop with Camera Gateway  

A camera gateway aggregates the camera streams and pushes the camera streams to the edge offices. This is requred if the link between the cameras and the edge offices is a 5G network. Camera gateway is for legacy IP cameras that do not support GB28181. IP cameras that support GB28181 can push streams to the edge office(s) without a camera gateway.   

The sample supposes dynamic starting/stopping of each office service and camera gateway, as follows:   

At the edge cloud/office cluster:   

```
cmake -DNOFFICES=2 ..
make

SCOPE=cloud make start_helm
SCOPE=office1-svc make start_helm
SCOPE=office2-svc make start_helm
...
SCOPE=office1-svc make stop_helm
...
SCOPE=office1-svc make start_helm
...
SCOPE=office1-svc make stop_helm
SCOPE=office2-svc make stop_helm
SCOPE=cloud make stop_helm
```

At the camera gateway:  

```
cmake -DNOFFICES=2 ..
make

SCOPE=office1-camera make start_helm
SCOPE=office2-camera make start_helm
...
SCOPE=office1-camera make stop_helm
SCOPE=office2-camera make stop_helm
```

### Database High Availability

Specify the following optional parameters for cloud or office database high-availability settings:

```
HA_CLOUD=3 make start_helm
...
HA_CLOUD=3 make stop_helm

HA_CLOUD=3 HA_OFFICE=3 make start_helm
...
HA_CLOUD=3 HA_OFFICE=3 make stop_helm
```

---

Each database instance requires about 2GB memory.   

---

