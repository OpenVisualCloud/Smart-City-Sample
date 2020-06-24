
The Smart City sample can be deployed with Kubernetes. 

### Kubernetes Setup

- Follow the [instructions](https://kubernetes.io/docs/setup) to setup your Kubernetes cluster. If you run into issues with Kubernetes/1.16 and Flannel/master, this [link](https://stackoverflow.com/questions/58024643/kubernetes-master-node-not-ready-state) might help.

- Optional: setup password-less access from the Kubernetes controller to each worker node (required by ```make update```):   

```
ssh-keygen
ssh-copy-id <worker-node>
```

- Start/stop services as follows:   

```
mkdir build
cd build
cmake ..
make
make update # optional for private docker registry
make start_kubernetes
make stop_kubernetes
```

---

The command ```make update``` uploads the sample images to each worker node. If you prefer to use a private docker registry, configure the sample, `cmake -DREGISTRY=<registry-url> ..`, to push images to the private registry after each build.  

---

### Multiple Office Start/Stop

The sample supposes dynamic office starting/stopping. You can selectively start and stop any office, as follows:

```
cmake -DNOFFICES=2 ..
make

SCOPE=cloud make start_kubernetes
SCOPE=office1 make start_kubernetes
SCOPE=office2 make start_kubernetes
...
SCOPE=office1 make stop_kubernetes
...
SCOPE=office1 make start_kubernetes
...
make stop_kubernetes  # cleanup all
```

### See Also 

- [Utility Scripts](../../doc/script.md)   
- [CMake Options](../../doc/cmake.md)
- [Helm Charts](helm/smtc/README.md)

