### Problem Statement

The smart stadium scenario focuses on different counting techniques, including entrance people counting, service-point queue counting, and stadium seating zone crowd counting. Each use case implemented different gva plugin, IR models and custom transform to suit for different counting requirement. We will compare them below. 

### Use Case Configuration
Please refer to [`CMake Options`](https://github.com/OpenVisualCloud/Smart-City-Sample/blob/master/doc/cmake.md) for detailed instructions on how to set up each use case.

### People Counting
People counting calculates how many people pass through the entrance in the past 5 secs. 
- [`gvadetect`](https://github.com/opencv/gst-video-analytics/wiki/gvadetect) plus [`person-vehicle-bike-detection-crossroad-0078`](https://docs.openvinotoolkit.org/2019_R1/_person_vehicle_bike_detection_crossroad_0078_description_person_vehicle_bike_detection_crossroad_0078.html) are used as the first step to detect people in the frame as bounding box;
- [`gvaclassify`](https://github.com/opencv/gst-video-analytics/wiki/gvaclassify) plus [`person-reidentification-retail-0079`](https://docs.openvinotoolkit.org/2018_R5/_docs_Retail_object_reidentification_pedestrian_rmnet_based_0079_caffe_desc_person_reidentification_retail_0079.html) are used to extract people's feature next;
- gvapython plus custom transform do the post processing for people counting with a sliding-window algorithm: the feature vector are saved in a pool with timestamp attached to each person. For each new frame, we compare the recently detected people with the people in the pool. If the person's feature is saved before, we just update his timestamp; otherwise, we push the new people's feature into the pool. At the end of each frame update, we loop around the pool, anyone disappears for more than 5 sec, we remove them out of the pool to keep the size small. 
```
cd build
cmake -DPLATFORM=Xeon -DSCENARIO=stadium -DNOFFICES=1 -DNCAMERAS=8,0,0 -DNANALYTICS=8,0,0 FRAMEWORK=gst ..
```
[[doc/stadium/smtc_people_counting.png]]

### Crowd Counting
Crowd counting calculates how many people seat in each seating zone in the stadium. We separate the stadium into 8 zones, East Wing, North East Wing, North Wing, North West Wing, West Wing, South West Wing, South Wing and South East Wing. Each zone is currently surveilled by one camera, but one camera can be expanded to surveil multiple zones by configuration.
- [`gvainference`](https://github.com/opencv/gst-video-analytics/wiki/gvainference) plus [`CSRNet model`](https://github.com/OpenVisualCloud/Smart-City-Sample/wiki/BKM:-Use-CSRnet-to-Count-Crowded-People) are used as the first step to detect total crowd number in the frame;
- gvapython plus custom transform do the post processing for crowd counting with a bitmask algorithm: a list of zone number and its polygons that covered by the camera are sending to the cumstom transform along with the crowd counting result on the whole frame. We make a bitmask for each zone, and count crowd number only inside the bitmask;
- to adjust bitmask for your own fixed camera, go [`sensor-info.json`](https://github.com/OpenVisualCloud/Smart-City-Sample/blob/master/maintenance/db-init/sensor-info.json) to add your own defined polygon;
- to define your own zonemap, go [`zonemap-37.39856d-121.94866.json`](https://github.com/OpenVisualCloud/Smart-City-Sample/blob/master/cloud/html/images/stadium/zonemap-37.39856d-121.94866.json) to add polygons for each zone.
```
cd build
cmake -DPLATFORM=Xeon -DSCENARIO=stadium -DNOFFICES=1 -DNCAMERAS=0,8,0 -DNANALYTICS=0,8,0 FRAMEWORK=gst ..
```
| Bitmask1| Bitmask2|
|:-------:|:-------:|
|<IMG src="doc/stadium/bitmask.png" width="100%"></IMG>|<IMG src="doc/stadium/bitmask2.png" width="100%"></IMG>|

[[doc/stadium/smtc_crowd_counting.png]] 

### Queue Counting
Queue counting calculates how many people are in the restaurant, meeting room, phone booth or elevator etc. 
- [`gvadetect`](https://github.com/opencv/gst-video-analytics/wiki/gvadetect) plus [`person-detection-retail-0013`](https://docs.openvinotoolkit.org/2018_R5/_docs_Retail_object_detection_pedestrian_rmnet_ssd_0013_caffe_desc_person_detection_retail_0013.html) are used to detect people in the frame as bounding box;
- It shares the same object-detection docker image with [`ad-insertion sample app`](https://github.com/OpenVisualCloud/Ad-Insertion-Sample). In the docker image, the two use cases share the same VA pipeline with different IR models. (Ad-insertion uses [`gvadetect`](https://github.com/opencv/gst-video-analytics/wiki/gvadetect) plus [`person-vehicle-bike-detection-crossroad-0078`](https://docs.openvinotoolkit.org/2019_R1/_person_vehicle_bike_detection_crossroad_0078_description_person_vehicle_bike_detection_crossroad_0078.html))
 
```
cd build
cmake -DPLATFORM=Xeon -DSCENARIO=stadium -DNOFFICES=1 -DNCAMERAS=0,0,8 -DNANALYTICS=0,0,8 FRAMEWORK=gst ..
```
[[doc/stadium/smtc_queue_counting.png]]

### Combined Use Cases
All three use cases can be combined together. Below is an example of 2 people counting, 2 crowd counting and 2 queue counting running together. You can move around real-time camera display screen, track the statistic window and look into each analytics result. Feel free to explore more.
```
cd build
cmake -DPLATFORM=Xeon -DSCENARIO=stadium -DNOFFICES=1 -DNCAMERAS=2,2,2 -DNANALYTICS=2,2,2 FRAMEWORK=gst ..
```
[[doc/stadium/smart_stadium1.png]]
[[doc/stadium/smart_stadium2.png]]
[[doc/stadium/smart_stadium3.png]]