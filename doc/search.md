The sample UI presents a search box that enables search database content:    
- On the home page, the users can search cameras properties, for example, the office location (the computing facilities where the cameras are connected to.)    
- On the office page, the users can search analytics algorithms and see their execution statuses.    
- On the recording page, the users can search recorded clips and review them.    

The search box implements the following search features:    
- Field Existance Search:   

Return records with a non-null or false value of the specified field.    
Example: ```sensor:*``` or ```sensor=*```    

- ID Search:

Return the record of the specified record ID.    
Example: ```_id="abcdefghijklmnopqrstuvwxyz"``` or ```_id='abcdefghijklmnopqrstuvwxyz'```   

- Numeric Search:   

Return records matching the numeric value of a search field.    
Examples: ```resolution.width>=320```, ```resolution.width>resolution.height*1.6```, or ```duration<4*60*1000```       

- Binary Search:   

Return records matching the binary value of a search field.    
Examples: ```streams.is_avc=true``` or ```streams.is_avc=false```       

- Date/Time Search:    

Return records matching the time of a search field:    
Examples: ```time>04/03/2019```, ```time>now-10000```, ```time>10:10:10pm```, or ```time>04/03/2019 22:10:10```   

- String Search:   

Return records matching the string or substring of a search field.    
Exact Match: ```sensor="camera"``` or ```sensor='camera'```       
Substring Match: ```sensor:"camera"``` or ```sensor:'camera'```       

- Geo-location Search:    

Return records based on the geo-location of a search field.    
Examples: ```office:[45,-122]``` or ```office:[45,-122,100]```   

- Complex Search:   

Return records for any logic combinations of simple searches.    
Example: ```duration>20 and time>10:10:10```    

- Where Search (available on the recording page):   

Return recordings whose analytics data meet certain criteria.      
Example: ```time>now-10000 where objects.detection.bounding_box.x_max-objects.detection.bounding_box.x_min>0.1```    

### Database Known Limitations  

- The database is configured as a development setup: single host and no replication. Usually, a database should be setup on multiple systems for horizonal scaling and high availability.   
- Each data type, such as recordings and analytics, is saved on a single index. Each index can hold a maximum of 2 billion records.
- The response of any database search is limited to 10,000 records. Rewrite [script/db_query.py](../script/db_query.py) with the [Scroll](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-request-scroll.html) API to overcome this limitation.   

