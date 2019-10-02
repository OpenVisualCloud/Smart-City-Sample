
The Smart City sample can be deployed with Kubernetes. 

### Kubernetes Setup

1. Follow the [instructions](https://kubernetes.io/docs/setup) to setup your Kubernetes cluster. If you run into issues with Kubernetes/1.16 and Flannel/master, this [link](https://stackoverflow.com/questions/58024643/kubernetes-master-node-not-ready-state) might help.

2. Follow the [instructions](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/vm-max-map-count.html) to increase the VM mapping threshold on every worker node.

3. Setup password-less acess from the Kubernetes controller to each worker node (required by ```make update```):   

```
ssh-keygen
ssh-copy-id <worker-node>
```

4. If you enable more than 1 office, label the worker nodes as follows:    
    - Label the nodes where cloud/office services can run, for example, ```cloud_zone=yes```, ```office1_zone=yes```, ```office2_zone=yes```, ```office3_zone=yes```, etc.
    - Label the nodes where recoding storage can be saved (disk space required), for example, ```cloud_storage=yes```, ```office1_storage=yes```, ```office2_storage=yes```, ```office3_storage=yes```, etc.

```
kubectl label node <worker-node> office1_zone=yes
kubectl label node <worker-node> office1_storage=yes
```

5. Finally, start/stop services as follows:   

```
make update
make start_kubernetes
make stop_kubernetes
```

Note: The command ```make update``` can be skipped if you have a private docker registry to host the sample images. In such case, please upload images before starting Kubernetes.   

### See Also 

- [Utility Scripts](../../doc/script.md)   

