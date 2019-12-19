
The cloud web service implements the following REST end points for UI operations:

| REST Service | Description |
| --- | --- |
| GET / | Get the HTML pages. |
| GET /api/health | Check if office is online. |
| GET /api/workload | Proxy to each office and return the office system workload. |
| GET /api/search | Search database and return the search results. |
| GET /api/stats | Search database and return the statistics. |
| GET /api/hint | Get search keyword hints. |
| GET /recording | Proxy to each office and return the requested recoding clip or thumbnail. |
