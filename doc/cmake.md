
Use the following definitions to customize the building process:   
- **PLATFORM**: Specify the target platform. Currently the only supported platform is ```Xeon```.   
- **NOFFICES**: Specify the number of offices in the deployment. Currently support 1-3 offices. To extend to more offices, define additional office GPS locations in [location.m4](../deployment/common/location.m4). See also how to setup [docker swarm](../deployment/docker-swarm/README.md).    
- **NCAMERAS**: Specify the number of cameras served in each office. Currently support 1-8 cameras. To extend to more cameras, define additional camera GPS locations in [location.m4](../deployment/common/location.m4).    
- **NSERVICES**: Specify the number of analytics instances running in each office.   

### Examples:   

```
cd build
cmake -DPLATFORM=Xeon ..
```

```
cd build
cmake -DNOFFICES=3 -DPLATFORM=Xeon ..
```
