
This document describes the steps required for the sample to work with the Intel VCAC-A accelerator(s).    

### Prerequisites for Docker Swarm:

Please follow the [instructions](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/VCAC-A) to:  
- [Setup the Intel VCAC-A node(s).](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/VCAC-A/README.md#setup-the-vcac-a)     
- [Setup the Intel VCAC-A node(s) as swarm worker(s).](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/VCAC-A/README.md#setup-the-vcac-a-as-swarm-node)     

### Prerequisites for Kubernetes:

Please follow the [instructions](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/VCAC-A) to:  
- [Setup the Intel VCAC-A node(s).](https://github.com/OpenVisualCloud/Dockerfiles/blob/master/VCAC-A/README.md#setup-the-vcac-a)     
- [Setup the Intel VCAC-A node(s) as Kubernetes worker(s).](https://github.com/OpenVisualCloud/Dockerfiles/tree/master/VCAC-A#setup-the-vcac-a-as-kubernetes-node)     

### Build Sample

Configure and build the sample to run analytics on Intel VCAC-A as follows:     

```sh
mkdir build
cd build
cmake -DPLATFORM=VCAC-A ..
make
make update
```

where `make update` transfers the built docker images to the workers nodes. This is optional if you plan to use private docker registry. Replace `make update` with your instructions to upload the images to your private docker registry.   

### Run Sample on Docker Swarm

```sh
make start_docker_swarm
make stop_docker_swarm
```

### Run Sample on Kubernetes:

```sh
make start_kubernetes
make stop_kubernetes
```

### See Also:

- [Setup Docker Swarm](../deployment/docker-swarm/README.md)
- [Setup Kubernetes](../deployment/kubernetes/README.md)

