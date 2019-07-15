from db_query import DBQuery

s = DBQuery(host="http://sdp-sawtooth02.jf.intel.com:9200", index="sensors")
s.update("lk6RI2sBeqw-XeJeNExb", {"status": "idle"})