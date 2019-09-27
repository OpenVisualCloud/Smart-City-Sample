
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
    - Label the nodes where office services can run, for example, ```office1_zone=yes```, ```office2_zone=yes```, ```office3_zone=yes```, etc.
    - Label the nodes where recoding storage can be saved, for example, ```office1_storage=yes```, ```office2_storage=yes```, ```office3_storage=yes```, etc.

```
kubectl label node <worker-node> office1_zone=yes
kubectl label node <worker-node> office1_storage=yes
```

5. Finally, start/stop services as follows:   

```
make update
make start_kubernetes
make expose_service
make stop_kubernetes
```

The command ```make update``` can be skipped if you have a private docker registry to host the sample images.  
The command ```make expose_service``` can be skipped if you have a load balancer or an ingress setup. In such case, add the [LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) or the [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress) block in [cloud-web.yaml.m4](cloud-web.yaml.m4). As a temporily solution for debugging purpose, ```make expose_service``` patches the ```cloud-web-service``` external IP. As a result, you can access to the sample UI via ```https://<host-ip>:8443```.

### See Also 

- [Utility Scripts](../../doc/script.md)   

