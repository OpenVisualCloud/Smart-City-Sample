
### Deploying Smart City Sample under Open Network Edge Services Software (OpenNESS)

The set of scripts deploy the Smart City sample under OpenNESS. Different from development, where all containers deploy to a single machine or a swarm of machines, the OpenNESS deployment requires that the containers be deployed to different networks in the cloud, on the edge and around the cameras. The deployment scripts are divided accordingly. See each folder for details.    

Deployment sequence:   
```
make start_openness_cloud
make start_openness_office1
make start_openness_office2
make start_openness_office3
make start_openness_camera
```

```
make stop_openness_cloud
make stop_openness_office1
make stop_openness_office2
make stop_openness_office3
make stop_openness_camera
```

