
Use the following definitions to customize the building process:
- **PLATFORM**: Specify the target platform. Currently the only supported platform is ```Xeon```.
- **NOFFICES**: Specify the number of offices in the deployment. Currently support 1-3 offices. See also how to setup [docker swarm](../deployment/docker-swarm/README.md).

### Examples:

```
cd build
cmake -DPLATFORM=Xeon ..
```

```
cd build
cmake -DNOFFICES=3 -DPLATFORM=Xeon ..
```
