
##### Requirements:

* pybatfish python libraries
* GitPython Python libraries (to be able to clone git repo where configs are located)

`pip3 install pybatfish`

`pip3 install GitPython`

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

##### Typical End to End Flow

![Screenshot](https://github.com/bodleytunes/jimiplugin-batfish/blob/dev/typical-end-to-end-flow.png)

##### Typical End to End Flow

![Screenshot](https://github.com/bodleytunes/jimiplugin-batfish/blob/dev/end-to-end-flow2.png)



##### Typical End to End Flow - RemoteConnectFortigate details

![Screenshot](https://github.com/bodleytunes/jimiplugin-batfish/blob/dev/1_batfish_download_connect_fortigate.png)

##### Typical End to End Flow - RemoteConnectDownload Config - (Fortigate save config)

![Screenshot](https://github.com/bodleytunes/jimiplugin-batfish/blob/dev/2_batfish-cfgbackupFortigateConnect.png)


##### Typical End to End Flow - git ops

![Screenshot](https://github.com/bodleytunes/jimiplugin-batfish/blob/dev/4_batfish-gitops-push.png)
##### Typical End to End Flow - Batfish connection

![Screenshot](https://github.com/bodleytunes/jimiplugin-batfish/blob/dev/5_batfish_connect.png)

##### Typical End to End Flow - Batfish Access/Policy Check

![Screenshot](https://github.com/bodleytunes/jimiplugin-batfish/blob/dev/6_batfish_access_check.png)

##### Typical End to End Flow - Batfish Traceroute

![Screenshot](https://github.com/bodleytunes/jimiplugin-batfish/blob/dev/7_batfish_traceroute_check.png)

##### Typical End to End Flow - Batfish Reachability

![Screenshot](https://github.com/bodleytunes/jimiplugin-batfish/blob/dev/8_batfish_reachability_check.png)
