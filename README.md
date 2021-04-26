
##### Requirements:

* pybatfish python libraries

`pip3 install pybatfish`

Requires running batfish server:
This example uses batfish running in Docker

##### Example docker-compose file:

docker-compose.yml

```
version: "3.4"
services:
  batfish:
    hostname: batfish
    image: batfish/allinone
    volumes:
      - ./data:/data
    tty: true
    ports:
      - 8888:8888
      - 9997:9997
      - 9996:9996
```