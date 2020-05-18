
### CMake Options:

Use the following definitions to customize the building process:   
- **REGISTRY**: Specify the URL of the privcay docker registry.    
- **PLATFORM**: Specify the target platform: `Xeon` or [`VCAC-A`](vcac-a.md).   
- **FRAMEWORK**: Specify the target framework: `gst` or `ffmpeg` , Now `gst` is enabled.   
- **SCENARIO**: Specify the sample scenario(s): `traffic`, `stadium`, or their combination `traffic,stadium`. As each scenario runs its own set of services and databases, it is recommended that you run multiple scenarios only on a multiple-node deployment setting.     
- **NOFFICES**: Specify the number of offices in the deployment. Support 1-3 offices in the traffic scenario and 1 office in the stadium scenario.       
- **NCAMERAS**: Specify the number of cameras served in each office. Currently support 1-8 cameras. In the **stadium** scenario, you can specify the camera numbers as `<#service_queue_counting>,[#crowd_counting],[#entrance_counting]`. 
- **NANALYTICS**: Specify the number of analytics instances running in each office. In the **stadium** scenario, you can specify different analytics instances with an additional number as `<#service_queue_counting>,[#crowd_counting],[#entrance_counting]`.  
- **NETWORK**: Specify the model network preference: `FP32`, `FP16`, `INT8`, or the combination of them.    

### Examples:   

```
cd build
cmake -DPLATFORM=Xeon ..
```

```
cd build
cmake -DNOFFICES=3 -DPLATFORM=Xeon ..
```

```
cd build
cmake -DPLATFORM=Xeon -DSCENARIO=traffic -DNOFFICES=3 -DNCAMERAS=5 -DNANALYTICS=3 FRAMEWORK=gst ..
```

```
cd build
cmake -DPLATFORM=Xeon -DSCENARIO=stadium -DNOFFICES=1 -DNCAMERAS=5,1,3 -DNANALYTICS=5,1,3 FRAMEWORK=gst ..
```

### Make Commands:

- **build**: Build the sample (docker) images.  
- **update**: Distribute the sample images to worker nodes.  
- **dist**: Create the sample distribution package.   
- **start/stop_docker_compose**: Start/stop the sample orchestrated by docker-compose.  
- **start/stop_docker_swarm**: Start/stop the sample orchestrated by docker swarm.   
- **start/stop_kubernetes**: Start/stop the sample orchestrated by Kubernetes.   
- **discover**: Scan the network specified by `PORT_SCAN` for IP cameras, and print out the IP camera profiles.    

### See Also:

- [Sample Distribution](dist.md)   
