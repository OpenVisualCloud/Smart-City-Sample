
The Smart City sample can be deployed with Kubernetes. 

### Kubernetes Setup

1. Follow the [instructions](https://kubernetes.io/docs/setup) to setup your Kubernetes cluster. If you run into issues with Kubernetes/1.16 and Flannel/master, this [link](https://stackoverflow.com/questions/58024643/kubernetes-master-node-not-ready-state) might help.

2. Setup password-less access from the Kubernetes controller to each worker node (required by ```make update```):   

```
ssh-keygen
ssh-copy-id <worker-node>
```

3. If you enable more than 1 office, label the worker nodes as follows:    
    - Label the nodes where cloud/office services can run, for example, ```cloud-zone=yes```, ```office1-zone=yes```, ```office2-zone=yes```, ```office3-zone=yes```, etc.
    - Label the nodes where recoding storage can be saved (disk space required), for example, ```cloud-storage=yes```, ```office1-storage=yes```, ```office2-storage=yes```, ```office3-storage=yes```, etc.

```
kubectl label node <worker-node> office1-zone=yes
kubectl label node <worker-node> office1-storage=yes
```

4. Finally, start/stop services as follows:   

```
mkdir build
cd build
cmake ..
make
make update
make start_kubernetes
make stop_kubernetes
```

---

The command ```make update``` uploads the sample images to each worker node. If you prefer to use a private docker registry, replace with your instructions to upload the images to your docker registry.   

---

### See Also 

- [Utility Scripts](../../doc/script.md)   
- [CMake Options](../../doc/cmake.md)
