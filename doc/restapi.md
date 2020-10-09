
The following table describes the REST API implemented at different services:  

|Type|Path|Descrption|Services|
|:---:|:---|:---|:---|
|`GET`|`api/search`|Perform the database search and return the content:<br>**`queries`**: The search string.<br>**`index`**: The DB index.<br>**`size`**: The return size. |web<br>cloud<br>office|
|`GET`|`api/histogram`|Perform the database search and return the bucketized values of the specified fields:<br>**`queries`**: The search string.<br>**`index`**: The DB index.<br>**`field`**: The field to be bucketized.<br>**`size`**: The max size.|web<br>cloud<br>office|
|`GET`|`api/stats`|Perform the database search and return the statistics (average, min, max) of the specified fields:<br>**`queries`**: The search string.<br>**`index`**: The DB index.<br>**`fields`**: The field list, comma delimited.|web<br>cloud<br>office|
|`GET`|`api/hint`|Retrieve search hints of the specified database index:<br>**`index`**: The DB indexe list, comma delimited|web<br>cloud<br>office|
|`GET`|`recording/...mp4`<br>`recording/...png`|Retrieve the sensor recording file in the `mp4` format, or the thumbail image in the `png` format.|web<br>cloud<br>office<br>storage|


