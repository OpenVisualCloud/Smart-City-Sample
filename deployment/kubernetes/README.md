
The sample can be deployed with Kubernetes. 

### Kubernetes Setup

Follow the [instructions](https://kubernetes.io/docs/setup) to setup your Kubernetes cluster. TIP: if you run into issues with Kubernetes/1.16 and Flannel/master, this [link](https://stackoverflow.com/questions/58024643/kubernetes-master-node-not-ready-state) might help.

Follow the [instructions](https://www.elastic.co/guide/en/elasticsearch/reference/6.8/vm-max-map-count.html) to increase the VM mapping threshold on every worker node.

Setup password-less acess from the Kubernetes controller to each worker node (requested by ```make update```):   

```
ssh-keygen
ssh-copy-id <worker-node>
```

If you enable more than 1 office, label the worker nodes as follows:
- Label the nodes where office services can run, for example, ```office1_zone=yes```, ```office2_zone=yes```, ```office3_zone=yes```, etc.
- Label the nodes where recoding storage can be saved, for example, ```office1_storage=yes```, ```office2_storage=yes```, ```office3_storage=yes```, etc.

```
kubectl label node <worker-node> office1_zone=yes
kubectl label node <worker-node> office1_storage=yes
```

Finally, start/stop services as follows:   

```
1. make update
2. make start_kubernetes
3. make expose_service
4. make stop_kubernetes
```

Step 1 above can be skipped if you have a private docker registry to host the sample images.  
Step 3 above can be skipped if you have a load balancer or an ingress setup. In such case, add the [LoadBalancer](https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer) or the [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress) block in [cloud-web.yaml.m4](cloud-web.yaml.m4). As a temporily debugging solution, ```make expose_service``` patches the ```cloud-web-service``` IP to be the controller IP. You can access to the sample UI via ```https://$(hostname):8443```.

### See Also 

- [Utility Scripts](../../doc/script.md)   

