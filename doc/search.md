
The sample is designed around database ingest and search:
- The sample UI presents a search box that enables search database content:    
  - On the home page, the users can search cameras properties, for example, the office location (the computing facilities where the cameras are connected to.)    
  - On the office page, the users can search analytics algorithms and see their execution statuses.    
  - On the recording page, the users can search recorded clips and review them.    

### Search Language  

The sample implements the following search features:    

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

- IP Address Search:

Return records based on the IP address of a search field.   
Examples: `ip=192.168.0.1` or `ip=192.168.0.0/16`   

- Complex Search:   

Return records for any logic combinations of simple searches.    
Example: ```duration>20 and time>10:10:10```    

### See Also:

- [The Ingest Script](../common/db_ingest.py)  
- [The Query Script](../common/db_query.py)   

