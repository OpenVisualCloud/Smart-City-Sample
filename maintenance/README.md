Live camera streaming is recorded in a 1min segment at the local storage. The following services are running to maintain the recording data:    
- **Indexing**: If any live analytics exist, they will be auto-indexed to match to the recorded data so users can perform 'where' queries on the recording data. See also [where query](../doc/search.md).   
- **Uploading**: Upload selected recording data, whose analytics data meet defined criteria, to cloud for archival or further processing/analysis. Transcoding to H.265 is done to save network bandwidth.       
