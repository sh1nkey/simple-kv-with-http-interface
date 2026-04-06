Features:
- set key and value (to save state between runs)
- get by unique identifier
- get by multiple unique identifiers


Implementation:
- set in dict + on disk
- get by key from dict
- get by keys from dict


HTTP/1.1 interface:
- set  POST /{key} + body as value, responds with 202
- get GET /{key}, responds with 200
- get many GET /{key},{key}, responds with 200