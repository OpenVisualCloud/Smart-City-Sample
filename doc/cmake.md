
Use the following definitions to customize the building process:   
- **PLATFORM**: Specify the target platform: ```Xeon``` or ```VCAC-A```.   
- **FRAMEWORK**: Specify the target framework: ```gst``` or ```ffmpeg``` , Now gst is enabled.   
- **SCENARIO**: Specify the sample scenario(s): ```traffic```, ```stadium```, or their combination ```traffic,stadium```. As each scenario runs its own set of services and databases, it is recommended that you run multiple scenarios only on a multiple-node deployment setting.     
- **NOFFICES**: Specify the number of offices in the deployment. Support 1-3 offices in the traffic scenario and 1 office in the stadium scenario.       
- **NCAMERAS**: Specify the number of cameras served in each office. Currently support 1-8 cameras. In the stadium scenario, you can specify an additional number as ```4,5```, which specifies that there are 4 cameras for people-counting and 5 cameras for crowd-counting.        
- **NANALYTICS**: Specify the number of analytics instances running in each office. Similarly, in the stadium scenario, you can specify different analytics instances with an additional number.      

### Examples:   

```
cd build
cmake -DPLATFORM=Xeon ..
```

```
cd build
cmake -DNOFFICES=3 -DPLATFORM=Xeon ..
```

