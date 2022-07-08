
### Introduction

Starting Kubernetes v1.20, Kubernetes deprecated docker as a runtime and used `containerd` instead. It is a prerequisite to install `containerd` before installing Kubernetes.

#### Installation

Install `containerd` from your OS packages:

```
apt-get install containerd       # Ubuntu or Debian
yum install containerd           # Centos
```

#### Setup Proxy

```
sudo mkdir -p /etc/systemd/system/containerd.service.d
printf "[Service]\nEnvironment=\"HTTP_PROXY=$http_proxy\" \"HTTPS_PROXY=$https_proxy\" \"NO_PROXY=$no_proxy\"\n" | sudo tee /etc/systemd/system/containerd.service.d/proxy.conf
sudo systemctl daemon-reload
sudo systemctl restart containerd
```

#### Setup Configuration Files

```
containerd config default | sudo tee /etc/containerd/config.toml
sudo systemctl restart containerd
```

#### Setup Insecure Registries

Optionally, follow the instructions if you need to setup any insecure registries, `foo.com:5000`:  

```
sudo sed -i 's|config_path =.*|config_path = "/etc/containerd/certs.d"|' /etc/containerd/config.toml

sudo mkdir -p /etc/containerd/foo.com:5000
cat | sudo tee /etc/containerd/certs.d/foo.com:5000/hosts.toml <<EOF
server = "http://foo.com:5000"
[host."http://foo.com:5000"]
  capabilities = ["pull", "resolve"]
[plugin."io.containerd.grpc.v1.cri".registry.configs."foo.com:5000".tls]
  insecure_skip_verify = true
EOF 
sudo systemctl restart containerd
```

#### Setup Data Storage

Optionally, if you need to move the containerd storage location to, for example, `/mnt/storage/containerd`:  

```
sed -i 's|^root =.*|root = "/mnt/storage/containerd"|' /etc/containerd/config.toml
sudo systemctl restart containerd
```

### See Also

- [Setup Kubernetes](setup-kubernetes.md)  

