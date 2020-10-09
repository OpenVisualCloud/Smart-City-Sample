
The following table describes the REST API implemented in different services:  

|Type|Path|Descrption|Services|
|:---:|:---|:---|:---|
|`GET`|`api/search`|Perform the database search and return the content:<br>`queries`: The [search](search.md) string.<br>`index`: The DB index.<br>`size`: The return size. |web<br>gateway|
|`GET`|`api/histogram`|Perform the database search and return the bucketized values of the specified fields:<br>`queries`: The [search](search.md) string.<br>`index`: The DB index.<br>`field`: The field to be bucketized.<br>`size`: The max size.|web<br>gateway|
|`GET`|`api/stats`|Perform the database search and return the statistics (average, min, max) of the specified fields:<br>`queries`: The [search](search.md) string.<br>`index`: The DB index.<br>`fields`: The field list, comma delimited.|web<br>gateway|
|`GET`|`api/hint`|Retrieve search hints of the specified database index:<br>`index`: The DB indexe list, comma delimited|web<br>gateway|
|`GET`|`recording/...mp4`<br>`recording/...mp4.png`|Retrieve the sensor recording file in the `mp4` format, or the thumbnail image in the `png` format.|web<br>gateway<br>storage|
|`POST`|`api/upload`|Upload the recorded file to the storage service.<br>`office`:The office location.<br>`sensor`:The sensor id.<br>`time`: The recording starting timestamp.|gateway<br>storage|
|`POST`|`api/tokens`|Create a token for subsequent webrtc operations:<br>`room`: The conference room id.|web<br>gateway<br>webrtc|
|`POST`|`api/sensors`|Create a conference room and import the specified sensor stream into the room.<br>`sensor`: The sensor id.|web<br>gateway<br>webrtc|
|`GET`|`api/auth`|Authenticate the user for access. Dummy implementation in the sample.|web|



