
### Prerequisite

Starting Kubernetes v1.20, Kubernetes deprecated docker as a runtime and used containerd instead. Follow the [instructions](setup-containerd.md) to install and configure `containerd` on your system.  

### Setup Kubernetes

Follow the [Ubuntu](https://phoenixnap.com/kb/install-kubernetes-on-ubuntu)/[CentOS](https://phoenixnap.com/kb/how-to-install-kubernetes-on-centos) instructions to setup a Kubernetes cluster. For full features, please install Kubernetes v1.21 or later.  

---

You can run the sample by setting up a single-node Kubernetes cluster:  

```
kubectl taint node --all node-role.kubernetes.io/master-
kubectl taint node --all node-role.kubernetes.io/control-plane-  # >= v1.20
```

---

### See Also

- [Setup Containerd](setup-containerd.md)   

