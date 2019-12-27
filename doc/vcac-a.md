
This document describes the steps required for the sample to work with the Intel VCAC-A accelerator(s).    

### Prerequisites

Please follow the [instructions](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/VCAC-A) to:  
- Setup the Intel VCAC-A node(s).     
- Setup the Intel VCAC-A as a swarm worker nodes.     

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
