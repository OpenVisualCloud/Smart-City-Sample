
This document describes the steps required for the sample to work with the Intel VCAC-A accelerator(s).    

### Prerequisites

Please follow the [instructions](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/VCAC-A) to setup the Intel VCAC-A node(s).     

### Docker Swarm Setup

Run the script [setup-vcac-a.sh](../script/setup-vcac-a.sh) to setup a local docker swarm cluster, which includes the following steps:
- Setup docker swarm master on the host.    
- Setup password-less access to the Intel VCAC-A node(s).
- Enroll the Intel VCAC-A worker node(s).   
- Label the Intel VCAC-A node(s).   


### Sample Configuration

Configure the sample to run analytics on Intel VCAC-A as follows:     

```sh
mkdir build
cd build
cmake -DPLATFORM=VCAC-A ..
make
make update
make start_docker_swarm
make stop_docker_swarm
```

### Known Limitations

- Support is limited to the docker swarm deployment. Kubernetes support is in development.    
