
There are two types of web services: the cloud web service is external facing and the local web service(s) is internal and specific to each office facility.

The cloud web service implements the following REST end points:

| REST Service | Description |
| --- | --- |
| GET / | Get the HTML pages. |
| GET /api/workload | Proxy to each office and return the office system workload. |
| GET /api/search | Search database and return the search results. |
| GET /api/stats | Search database and return the statistics. |
| GET /api/hint | Get search keyword hints. |
| GET /recording | Proxy to each office and return the requested recoding clip or thumbnail. |

The local web service implements the following REST end points:

| REST Service | Description |
| --- | --- |
| GET /api/workload | Proxy to each office and return the office system workload. |
| GET /recording | Proxy to each office and return the requested recoding clip or thumbnail. |


